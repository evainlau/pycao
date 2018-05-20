
from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
import povrayshoot 
from cameras import *
from lights import *
import povrayshoot

"""
################
Objects considered
################
PNFITem = a string called smallsting+ a facultative moveMap attribute ( Fitems never have this attribute)
Titem= [ a list of PNFT items ]+ a moveMap. Only the first element may be a texture, in which case it is a named texture
accessed with an iedentfier. A texture is defined by its list of elements, execpt for the texture at the base 
of the recursion which are defined by a string and that we call stringy. Non stringy textures are called recursive, they
correspond to lists with lengths at least 2. 

################                
Moving textures
################

Methods to move an element:
PNF itemss and stringy TItems: change the movemap
Non stringy tItems: move each item in the list

################
INPUT 
################
* string Titems and PNF items : the smallString which is a sting considered by povray without the pigment{..} or texture{...} 
surrounding it. May also be the name of a previously defined (in the code or in pivray) PNFT item .

* Recursive T-item : the list of items it contains. 
In particular, there is no string in the input besides the special case of predefined povray texture (they are called "stringy" below).
Summing up, we have roughly input=strings for PNF-items and items not string for T-items.

################
Naming and declaration
################
Each structure can be declared to make the povray code more readable. What a structure is named, 
it is automatically declared as a by product. At the moment it is declared, it becomes stringy. 
Sometimes, it is necessary to declare a name to be compatible with povray's internals. 
The name built  automatically depends on the pidname and the date to avoid collisions 
when the same object is declared several times. 

Some textures (like the cubic pattern), don't support finishes 
or matrix identifier (povray limitation), but they can be 
declared and then enhanced by a finish or moved. 
Correspondingly, these textures must be named to be 
operational with our formalism.  

Povray does not admit a string like "texture {texture {keyword matrixMove} otherItems}" but only 
"texture { nameOfDeclaredTexture otherItems}". Thus some automatic declaration is 
sometimes required to fullfill povray input format. 


################
Outputs
################

All objects considered here, aka pnft items, must produce a string to povray at different occasions. The string depdends on 
- whether the objecti is declared in povray or not (solved by changing the smallString atribute when declaring an object)
- the context ( in a declaration string or nested within a surronding texture in povrayshoot ( unnested_output et nested_output) 
- the instance (PNF items have different rules than T items)
- if we want to include the displacement matrinx  or not in the  string ( withMove=True or False) 

___________________________________________________________________________________________________________________________________________
          |                                                        |                                                                     |
          |             unnamed                                    |                          named                                      |
__________________________________________________________________________________________________________________________________________
          |                                                        |                                                                     |
          |         pigment {smallString moveString}               |                 pigment {name movestring}                           |
          |                                                        |                                                                     |
          |         texture {smallString moveStrting} (stringy)    |                 texture {name movestring}                           |
unnnested                 
          |   texture{nestedOutput(t1)...} for t=[t1,...]          |               (A named texture is stringy, thus non recursive)      |
______________________________________________________________________________________________________________________________
          |                                                        |                                                                     |
          |           pigment { smallString movestring}            |                     pigment {name movestring}                       |
          |                                                        |                                                                     |
nested    |
          |          impossible for textures which must            |                     name ( no movestring possible                   |
          |          appear as named textures when                 |                     the move string must be included                |
          |          nested inside a englobing texture             |                     in the declaration of name)                     |
          |                                                        |                                                                     |
          |                                                        |                   (emed textures are not recursive )                |
________________________________________________________________________________________________________________________________

################
Enhancements
################

When a pnft item has been named, its shortstring is equal to its name. To enhance, we enhance the shortstring
for pnf items and we add an element to the list in the case of textures (stringy or recursive)

"""


class PNFTItem(object):#PNF means Pigment,Normal or Finish or texture

    def build_and_get_idname(self):
        """ constructs a string based on time to be used as identifier """
        import time
        return "Id"+str(int(round(time.time() * 100000)))

    def moveString(self):
        if hasattr(self,"moveMap"):
            moveString=" matrix "+povrayshoot.povrayMatrix(self.moveMap)
        else: moveString=" "
        return moveString

    def declare(self, name=None, withMove=True):
        if name is None:
            name=self.build_and_get_idname()
        globvars.TextureString+="\n#declare "+name+" = "+self.unnested_output(withMove=withMove)
        self.__init__(name) #reinitialisation from the name
        return self

    def output_from_small_string(self,withMove):
        return self.__class__.__name__.lower()+" {"+self.smallString+" "+self.moveString()+"}"

    def __str__(self):
        #print(len(self))
        #print(self.__class__)
        return  self.unnested_output(withMove=True)

    
class PNFItem(PNFTItem):#PNF means Pigment,Normal or Finish
    def __init__(self,string):
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} 

    def nested_output(self,withMove):
        return self.output_from_small_string(withMove=withMove)

    def unnested_output(self,withMove):
        return self.output_from_small_string(withMove=withMove)
        
    def enhance(self,stringOrPNFItem):
        """
        takes a copy of self, adds the stringOrPNFItem options, and returns the modified copy
        This may be used to add diffuse or ambient options in a finish, or a transformation in a pigment,normal, etc... 
        """
        def _tostring(a):
            if isinstance(a,str):
                return a
            else:
                return a.smallString
        stringToAdd=" "+_tostring(stringOrPNFItem)
        self.smallString += stringToAdd
        return self

    def move(self,mape,name=""):
        if isinstance(self,Finish):
            pass
        else:
            try:
                self.moveMap=mape*self.moveMap
            except: #probably not moved yet and no movemap defined
                self.moveMap=mape
            return self
        
        
class Pigment(PNFItem):
    def __init__(self,string):
        super(Pigment,self).__init__(string)

    @staticmethod
    def from_photo(pngfilepath,dimx=1.,dimy=1.,normal=None,corner=None):
        """returns a pigment which is a a wall paper on each plane z=cte, 
        and the photo is a rectangle of size dimx by dimy on this plane. 
        If normal is given, the wallpapers are planes orthogonal to the normal vector instead of planes z=cte.
        If corner is given, the wall papers are translated so that the bottom left corner of the photo appears at corner. 
        """
        if dimx is None: dimx=1. # mabe coming from other subroutines 
        if dimy is None: dimy=1.
        p=Pigment("image_map {png \""+pngfilepath+"\" }").move(Map.linear(dimx*X,dimy*Y,Z))
        if normal is not None:
            mape=Map.rotational_difference(Z,normal)
            p.move(mape)
        if corner is not None:
            map=Map.translation(corner-origin)
            p.move(mape)
        return p
            
                  
class Normal(PNFItem):
    def __init__(self,string):
        super(Normal,self).__init__(string)

class Finish(PNFItem):
    def __init__(self,string):
        super(Finish,self).__init__(string)


class Texture(PNFTItem,list):


    def nested_output(self,withMove):
        # must return the name, so build the name if necessery
        #print("theSmallString")
        return self.smallString 

    def unnested_output(self,withMove=True):
        if self.stringy:
            #print("yes stringy")
            #print(self.smallString)
            return self.output_from_small_string(withMove)
        else: #recursive case
            #print("inUnnested non stringy le with move vaut",withMove)
            string=" ".join([entry.nested_output(withMove=withMove) for entry in self])
            return "texture {"+string+"}"

    def maybe_declare_first_argument(self):
            if not self.stringy and isinstance(self[0],Texture) and (hasattr(self[0],"moveMap") or (not self[0].stringy) or  len(self[0].smallString.split())>1):
                self.declare(withMove=True)


    def move(self,mape):
        if self.stringy: # stringy, no recursion occurs
            try:
                self.moveMap=mape*self.moveMap
            except: #probably not moved yet and no movemap defined
                self.moveMap=mape
        else: #non stringy 
            [entry.move(mape) for entry in self]
        return self
            
    def __new__(cls,*args,**kwargs):
        return list.__new__(cls)
            
    def __init__(self,*args):
        #if len(args)==0:
        #    raise nameError("0 argument")
        if len(args)==1 and isinstance(args[0],str):
            #self.stringy=True #?? not used it seems
            #print("les args")
            #for l in args:
            #    print(l )
            #print("fin")
            self.stringy=True
            self.smallString=args[0] # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{}
            #self.append(self)
        else:
            #print(args)
            self.stringy=False
            for entry in args:
                self.append(entry)
            #self.maybe_declare_first_argument

    @staticmethod
    def from_colorkw(ckw):
        return Texture("pigment {color "+ckw+"}")


    def enhance(self,pnfitem):
        #print("enhanced by",pnfitem)
        if isinstance(pnfitem,PNFTItem):
            if not self.stringy:
                self.append(pnfitem)
            else:
                self.append(self.copy())
                self.append(pnfitem)
                self.stringy=False #unuseful I think, but clarifies
                #self.maybe_declare_first_argument()
        else: raise NameError("A structure is enhanced by a texture, a pigment, or a finish, not "+type(pnfitem).__name__)
        #print("inenhance")
        #print(type(self[0]))
        return self

    def copy(self):#no deepcopy needed since contains only strings
        memo=dict()
        return copy.deepcopy(self,memo)    

    @staticmethod
    def from_cubic_photos(dimx,dimy,dimz,photo1=None,photo2=None,photo3=None,photo4=None,photo5=None,photo6=None,xscaleFactor=None,yscaleFactor=None,grainVector=Z):
        """
        This function returns a texture to be applied to a cube of dimension of the parameters     centered at origin.
        The grain Vector is by default in the Z direction, ie. the four facets around the Z axis have an orientation like pictures 
        glued around the 4 walls of a building. May be replaced by X or Y in the parameters.
        Photos are given in png format by their path.
        photo1,2,3,4,5,6 correspond to face -X,-Y,-Z,X,Y,Z. Photo1 must be given. If missing the other photos are copied from the opposite face
        or from photo1. 
        The scaleFactore acts on the image (for instance to make the grain of the wood more or less dense.
        """
        if photo2 is None:
            photo2=photo1
        if photo3 is None:
            photo3=photo1
        if photo4 is None:
            photo4=photo1
        if photo5 is None:
            photo5=photo2
        if photo6 is None:
            photo6=photo3
        if grainVector==X:
            mape=Map.linear(Z,Y,X)
            d=dimx;dimx=dimz;dimz=d
        if grainVector==Y:
            mape=Map.linear(X,Z,Y)
            d=dimy;dimy=dimz;dimz=d
        s=xscaleFactor
        t=yscaleFactor
        pigment1=Pigment.from_photo(photo1,s,t).move(Map.affine(-1./dimy*X,1/dimz*Y,Z,(.5+dimy*2.)*X+(.5+dimz*2.)*Y))
        pigment2=Pigment.from_photo(photo2,s,t).move(Map.affine(-1./dimx*X,1/dimz*Y,Z,(.5+dimx*2.)*X+(.5+dimz*2.)*Y))
        pigment3=Pigment.from_photo(photo3,s,t).move(Map.affine(-1./dimx*X,1/dimy*Y,Z,(.5+dimx*2.)*X+(.5+dimy*2.)*Y))
        pigment4=Pigment.from_photo(photo4,s,t).move(Map.affine(-1./dimy*X,1/dimz*Y,Z,(.5+dimx*2.)*X+(.5+dimy*2.)*Y))
        pigment5=Pigment.from_photo(photo5,s,t).move(Map.affine(-1./dimx*X,1/dimz*Y,Z,(.5+dimx*2.)*X+(.5+dimy*2.)*Y))
        pigment6=Pigment.from_photo(photo6,s,t).move(Map.affine(-1./dimx*X,1/dimy*Y,Z,(.5+dimx*2.)*X+(.5+dimy*2.)*Y))
        planarTexture1=Texture(pigment1).move(Map.rotation(Y,math.pi*.5)).move(Map.rotation(X,math.pi*.5)).unnested_output()
        planarTexture4=Texture(pigment4).move(Map.rotation(Y,math.pi*.5)).move(Map.rotation(X,math.pi*.5)).unnested_output()
        planarTexture2=Texture(pigment2).move(Map.rotation(X,math.pi*.5)).unnested_output()
        planarTexture5=Texture(pigment5).move(Map.rotation(X,math.pi*.5)).unnested_output()
        planarTexture3=Texture(pigment3).unnested_output()
        planarTexture6=Texture(pigment6).unnested_output()
        cubicTex=Texture("cubic "+ planarTexture1 +" ,"+ planarTexture2 +" ,"+ planarTexture3+" ,"+planarTexture4+" ,"+planarTexture5+" ,"+planarTexture6) 
        cubicTex.move(Map.scale(dimx,dimy,dimz))
        if grainVector==Y or grainVector==X:
            cubicTex.move(mape)
        return cubicTex


def unleash(liste):
    texture=liste[0].texture
    for obj in liste:
        if not obj.texture==texture:
            raise NameError("All objects must share the same texture to unleash it")
    newtexture=texture.copy()
    for obj in liste:
        obj.new_texture(newtexture)

def _new_texture(self,texture):
    if isinstance(texture,str):#then should be a povray name texture
        texture=Texture(texture)
    self.texture=texture
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                _new_texture(slave,texture)
    return self

def _add_to_texture(self,value):
    if hasattr(self,"texture"):
        self.texture.enhance(value)
    else:
        self.texture=Texture(value)
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                try:
                    if not slave.texture==self.texture:#otherwise already done
                        _add_to_texture(slave,value)
                except:
                    pass #slave has no texture
    return self


def _get_textures(self,texturelist=None,withChildren=True,maybeDeclare=False):
    if texturelist is None:
        texturelist=[]
    try:
        texturelist.append(self.texture)
        if maybeDeclare:
            self.texture.maybe_declare_first_argument()
        pass
    except: # no texture
        pass
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            for slave  in op.csgSlaves :
                for entry in slave.get_textures():
                    if entry not in texturelist:#id necessary to avoid infinite loop
                        texturelist.append(entry)
                        if maybeDeclare:
                            entry.maybe_declare_first_argument()
                        
                #except: pass # notexture for the slave
    if withChildren:
        for c in self.children:
            c.get_textures(texturelist=texturelist,maybeDeclare=maybeDeclare)
    return texturelist

def build_textures_for_list(liste):
    texturelist=[]
    for entry in liste:
        entry.get_textures(texturelist,withChildren=True,maybeDeclare=True)
    return texturelist

def _colored(self,color):
    " color should be a string known to povray"
    p=Pigment(color)
    #print(p.smallString)
    if hasattr(self,"texture"):
        t=self.texture.enhance(p)
        #print(t)
        #print(self.texture)
    else:
        t=Texture(p)
        self.new_texture(t)#keep it for the childs in csg    #print(self.texture.smallString)
    #print("phasname",p.name)
    #print("in colored",t.smallString)
    return self

ObjectInWorld.colored=_colored
ObjectInWorld.new_texture=_new_texture
ObjectInWorld.add_to_texture=_add_to_texture
ObjectInWorld.get_textures=_get_textures
        
"""
unleash code tested:
c=Sphere(origin,.1)
d=Sphere(origin+.2*X,.1)
e=Sphere(origin+.4*X,.1)
d.texture=c.texture
e.texture=c.texture
c.colored("Blue")
import material
material.unleash([d,e])
d.colored("Green")
material.unleash([c,d])
"""
        
#def defaultTexture():
#    return Texture("pigment {Yellow}")

photo1="image_map {png \"hugoMathisRobin.png\"}"
photo2="image_map {png \"annivHugo.png\"}"
photo3="image_map {png \"chene.png\" }"

#pigment3=Pigment("image_map {png \"chene.png\" }").move(Map.scale(2*scale1,2*scale2,1)).move(Map.translation(scale1*Y))

 



def cubic_oak(scale1,scale2,scale3):
    """
    This function returns a texture for a cube of dimension of the parameters and grain Vector in the Z direction. 
    The file "chene.png" may be replaced by an other file where the grain vector is in the Y direction. 
    """
    print(scale1,scale2/2.,"sc1 et 2")
    pigment1=Pigment(photo3).move(Map.affine(-scale2*X,scale3*Y,Z,(.5+1/scale2*2.)*X+(.5+1/scale3*2.)*Y))#-scale2/8.*X+scale3/8.*Y))#1*(scale1*X+scale2*Y)))
    pigment2=Pigment(photo3).move(Map.affine(-scale1*X,scale3*Y,Z,(.5+1/scale1*2.)*X+(.5+1/scale3*2.)*Y))
    pigment3=Pigment(photo3).move(Map.affine(-scale1*X,scale2*Y,Z,(.5+1/scale1*2.)*X+(.5+1/scale2*2.)*Y))
    #oakPlanarTannivHugo.pngexture1="texture{pigment {} rotate -90*y rotate 90*x scale "+str(scale1)+"} ," #the grain is along Y
    #oakPlanarTexture2="texture{pigment {image_map {png \"chene.png\"  }} rotate -90*x scale "+str(scale2)+"} ,"
    #oakPlanarTexture3="texture{pigment {image_map {png \"chene.png\"  }} scale " +str(scale3)+" } ," 
    oakPlanarTexture1=Texture(pigment1).move(Map.rotation(Y,math.pi*.5)).move(Map.rotation(X,math.pi*.5)).unnested_output()+" ,"
    oakPlanarTexture2=Texture(pigment2).move(Map.rotation(X,math.pi*.5)).unnested_output()+" ,"
    oakPlanarTexture3=Texture(pigment3).unnested_output()+" ,"
    oakCubicTexture=Texture("cubic "+ oakPlanarTexture1 + oakPlanarTexture2 + oakPlanarTexture3+oakPlanarTexture1+oakPlanarTexture2+oakPlanarTexture3)#.declare("cubicOak")
    return oakCubicTexture
    
oakImage=Pigment("image_map {png \"chene.png\" }").move(Map.rotation(Y,math.pi/2)).move(Map.rotation(X,math.pi/2))
#scale1=.3
#scale2=.6
#scale3=3
colorTexture="texture{ pigment{color rgb<1.0 , 0.4, 0.0>}}"
#oakPlanarPigment=" color rgb<1.0, 0.0, 0.0>,"
#print ("avtOKT")


#print("apresOKT")
oakCylindricalTexture=Texture("pigment {image_map {png \"chene.png\" map_type 2 }}")
oakTexture=Texture("pigment {image_map {png \"chene.png\" }}")
#oakCubicTexture=oakTexture
wengeTexture=Texture("pigment {image_map {png \"wenge.png\" }}")
