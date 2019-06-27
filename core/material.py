
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
The textures in Povray are a bit messy. The following tries to define an implementatin in pycao which 
is workable easily ( for instance for zooming the textures, overriding them partially, gluing them so that they follow 
a moving objects.... ) , yet being compatible  with povray without headaches. There is a balance between 
a complete python approach which would generate an unworkable ugly povray code, and a gentle povray code,  
including declarations of stuctures for readability, but carrying the corresponding limitations ( for instance,  Povray does 
not admit a string like "texture {texture {keyword matrixMove} otherItems}" but only  
"texture { nameOfDeclaredTexture otherItems}". Thus some automatic declaration is 
sometimes required to fullfill povray input format. )


A texture is a recursive structure. It is defined by its list of elements. The texture at the base 
of the recursion are defined by a string and  we call them stringy textures. Non stringy textures are called recursive, they
correspond to lists with lengths at least 2. 

In contrast to textures, pigments, normal and finishes (PNF) are not recursive. But they can be used recursivly once they are embedded 
in a texture. 

Formally,
PNF ITem = P(igment)N(ormal)(or)F(inish)Item=elementary entity corresponding to a pigment or normal or finish in povray=  a string called smallsting+ a facultative moveMap attribute ( Finish items never have a move map)
Titem= T(exture)Item= [ a list of PNF or T items ]+ a moveMap. Only the first element may be a texture, in which case it is a named texture
accessed with an identifier ( for povray compatibility). For recursive Titems, the move map is identity (each element in the list is moved individually).

Obviously, this is limitative as T=[Texture1,Texture2] is not allowed is not a valid input whereas T=[nameOfDeclaredTexture1, item1 of texture2, item2 of textur2...]
is valid. A fully recursive definition of textures may be possible in the future, but it requires some more code for povray compatibility. One needs to flatten out 
the recursive tree to build a string understandable by povray.  This is not difficult, but if we flatten out everything, the povray code becomes terrific and ugly.  Thus for the moment, I keep this limitation with readable povray code as I don't have a clear view of what I want.  The problem is : what to do with texture{ namedTexture1, namedTexture2 } whereas povray does not allow two named textures. 


################
INPUT 
################
* stringy Titems and PNF items : the smallString which is a sting considered by povray without the pigment{..} or texture{...} 
surrounding it. May also be the name of a previously defined (in the code or in pivray) PNFT item .

* Recursive T-item : the list of items it contains.  Each element in the list is a pycao object defined before or a string corresponding 
to a predefined povray texture, or a string for a pycao object declared to povray (see below).
Summing up, we have roughly input=strings for PNF-items, a string for stringy T-items, ( converted to a list with a unique element by pycao), 
 lists for recursive T-items.

################                
Moving textures
################

Methods to move an element:
PNF items and stringy TItems: change the movemap
Non stringy TItems: move each item in the list

################
Naming and declaration
################
Each structure can be declared to make the povray code more readable. When a structure is named, 
it is automatically declared as a by product. At the moment it is declared, it becomes stringy. 
Sometimes, it is necessary to declare a name to be compatible with povray's internals. 
The name built  automatically depends on the pidname and the date to avoid collisions 
when the same object is declared several times. 

Some textures (like the cubic pattern), don't support finishes 
or matrix identifier (povray limitation), but they can be 
declared and then enhanced by a finish or moved. 
Correspondingly, these textures must be named to be 
operational with our formalism.  



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


class PNFTItem(ObjectInWorld):#PNF means Pigment,Normal or Finish or texture

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
        if withMove and hasattr(self,"moveMap"):
            del self.moveMap
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

    def unnested_output(self,withMove=True):
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
    def from_photo(pngfilepath,dimx=1.,dimy=1.,normal=None,center=None,symmetric=False):
        """returns a pigment which is a a wall paper on each plane z=cte, 
        and the photo is a rectangle of size dimx by dimy on this plane. 
        If normal is given, the wallpapers are planes orthogonal to the normal vector instead of planes z=cte.
        If center is given, the wall papers are translated so that the center of the photo appears there. 
        """
        if dimx is None: dimx=1. # mabe coming from other subroutines 
        if dimy is None: dimy=1.
        p=Pigment("image_map {png \""+pngfilepath+"\" }")
        if symmetric:
            p=p.symmetrised_clone()
        if center is not None:
            map=Map.translation(center-.5*X-.5*Y-.5*Z)
            p.move(map)
        p.move(Map.linear(dimx*X,dimy*Y,Z))
        if normal is not None:
            mape=Map.rotational_difference(Z,normal)
            p.move(mape)
        return p

    @staticmethod
    def from_square(p1=None,p2=None,p3=None,p4=None):
        """ 
        corresponds to the povray square pattern. Useful for a piece of wood for instance where the pigment depend on the face.
        """
        if p1 is None: p1=Pigment("Red")
        if p2 is None: p2=Pigment("Green")
        if p3 is None: p3=Pigment("Blue")
        if p4 is None: p4=Pigment("Yellow")
        argument="square "+" ".join([p.unnested_output(withMove=True) for p in [p1,p2,p3,p4]])
        return Pigment(argument)
    
    def symmetrised_clone(self,dimx=1,dimy=1,normal=None,corner=None):
        """
        input=a pigment in the plane x,y  in the square with opposite corners 0,0 and 1,1
        output by default=a pigment in the square with opposite corners 0,0 and 1,1 obtained by symmetrisation
        if dimx and dimy are filled, the square is redimensioned to a rectangle
        If normal is given, the wallpapers are planes orthogonal to the normal vector instead of planes z=cte.
        If corner is given, the wall papers are translated so that the bottom left corner of the photo appears at corner. 
        """
        M=Map.rotation(X,math.pi/2)
        p1=self.move(M) # from the xy plane to the xz plane
        p4=p1.clone().flipX()
        #print("p1p2")
        #print(p1)
        #print(p2)
        p3=p1.clone().flipZ().flipX()
        p2=p1.clone().flipZ()
        p=Pigment.from_square(p1,p2,p3,p4)
        p.move(M.inverse())#back to the xy plane
        p.scale(.5*dimx,.5*dimy,1)
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
                self.append(self.clone())
                self.append(pnfitem)
                self.stringy=False #unuseful I think, but clarifies
                #self.maybe_declare_first_argument()
        else: raise NameError("A structure is enhanced by a texture, a pigment, or a finish, not "+type(pnfitem).__name__)
        #print("inenhance")
        #print(type(self[0]))
        return self

    def clone(self):#no deepcopy needed since contains only strings
        memo=dict()
        return copy.deepcopy(self,memo)    

    @staticmethod
    def from_photo(pngfilepath,dimx=1.,dimy=1.,normal=None,center=None,symmetric=False):
        p=Pigment.from_photo(pngfilepath=pngfilepath,dimx=dimx,dimy=dimy,normal=normal,center=center,symmetric=symmetric)
        return Texture(p)
        
    @staticmethod
    def from_cubic_photos(dimx,dimy,dimz,photo1=None,photo2=None,photo3=None,photo4=None,photo5=None,photo6=None,xscale=None,yscale=None,grainVector=Z,symmetric=True):
        """
        This function returns a texture to be applied to a cube of dimension of the parameters     centered at origin.
        The grain Vector is by default in the Z direction, ie. the four facets around the Z axis have an orientation like pictures 
        glued around the 4 walls of a building. May be replaced by X or Y in the parameters.
        Photos are given in png format by their path.
        photos 1,2,3,4,5,6 correspond to face -X,-Y,-Z,X,Y,Z. Photo1 must be given. If missing the other photos are copied from the opposite face
        or from photo1. 
        The scalee acts on the image (for instance to make the grain of the wood more or less dense.
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
             d=dimx;dimx=dimz;dimz=d
             ret=Texture.from_cubic_photos(dimx,dimy,dimz,photo1=photo3,photo2=photo2,photo3=photo1,photo4=photo6,photo5=photo5,photo6=photo1,xscale=xscale,yscale=yscale,grainVector=Z,symmetric=symmetric)
             return ret.flipXZ()
        if grainVector==Y:
            d=dimy;dimy=dimz;dimz=d
            ret=Texture.from_cubic_photos(dimx,dimy,dimz,photo1=photo1,photo2=photo3,photo3=photo3,photo4=photo4,photo5=photo6,photo6=photo5,xscale=xscale,yscale=yscale,grainVector=Z,symmetric=symmetric)
            return ret.flipYZ()
        if not grainVector==Z:
            raise NameError("The grain Vector must be X,Y or Z")
        s=xscale
        t=yscale
        pigment1=Pigment.from_photo(photo1,s,t,normal=X,center=origin,symmetric=symmetric)
        pigment1.rotate(X,math.pi/2).scale(1./dimx,1./dimy,1./dimz)
        pigment2=Pigment.from_photo(photo2,s,t,normal=Y,center=origin,symmetric=symmetric)
        pigment2.rotate(Y,math.pi).scale(1./dimx,1./dimy,1./dimz)
        pigment3=Pigment.from_photo(photo3,s,t,normal=Z,center=origin,symmetric=symmetric)
        pigment3.scale(1./dimx,1./dimy,1./dimz)
        pigment4=Pigment.from_photo(photo4,s,t,normal=X,center=origin,symmetric=symmetric)
        pigment4.rotate(X,math.pi/2).scale(1./dimx,1./dimy,1./dimz)
        pigment5=Pigment.from_photo(photo5,s,t,normal=Y,center=origin,symmetric=symmetric)
        pigment5.rotate(Y,math.pi).scale(1./dimx,1./dimy,1./dimz)
        pigment6=Pigment.from_photo(photo6,s,t,normal=Z,center=origin,symmetric=symmetric).scale(1./dimx,1./dimy,1./dimz)
        planarTexture1=Texture(pigment1).unnested_output()
        planarTexture4=Texture(pigment4).unnested_output()
        planarTexture2=Texture(pigment2).unnested_output()
        planarTexture5=Texture(pigment5).unnested_output()
        planarTexture3=Texture(pigment3).unnested_output()
        planarTexture6=Texture(pigment6).unnested_output()
        cubicTex=Texture("cubic "+ planarTexture1 +" ,"+ planarTexture2 +" ,"+ planarTexture3+" ,"+planarTexture4+" ,"+planarTexture5+" ,"+planarTexture6) 
        cubicTex.move(Map.scale(dimx,dimy,dimz))
        return cubicTex




    
def unleash(liste):
    """ useful if a texture applies to o1, o2,... and you want to move o2,o3.. with the texture without changing the texture of o1.  Then unleash o2,o3..."""
    texture=liste[0].texture
    for obj in liste:
        if not obj.texture==texture:
            raise NameError("All objects must share the same texture to unleash it")
    newtexture=texture.clone()
    for obj in liste:
        obj.new_texture(newtexture)
        
def remove_texture(self):
    try:
        del self.texture
    except: pass
    return self

def new_texture(self,texture):
    if isinstance(texture,str):#then should be a povray name texture
        texture=Texture(texture)
    self.texture=texture
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                new_texture(slave,texture)
    return self

def add_to_texture(self,value):
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
    if hasattr(self,"texture"):
        texturelist.append(self.texture)
        if maybeDeclare:
            self.texture.maybe_declare_first_argument()
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            for slave  in op.csgSlaves :
                for entry in slave.get_textures():
                    if id(entry) not in [id(t) for t in texturelist]:#id necessary since textures with the same entries may be different
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


def _rgbed(self,*args):
    #print("inrgbed1",self.texture.smallString)
    if len(args)==1:#then arguments given as a list wich is args[0]
        textArgs=[str(t) for t in args[0]]
    else:
        textArgs=[str(t) for t in args]
    argument=",".join(textArgs)
    p=Pigment("color rgb <"+argument+">")
    if hasattr(self,"texture"):
        t=self.texture.enhance(p)
    else:
        t=Texture(p)
    self.new_texture(t) #for the csg childs
    return self

def _light_level(self,value):
    ambient=value*defaultAmbientMultiplier
    diffuse=value*defaultDiffuseMultiplier
    finish=Finish("ambient "+str(ambient)+" diffuse "+str(diffuse))        
    self.add_to_texture(finish)
    return self



ObjectInWorld.colored=_colored
ObjectInWorld.remove_texture=remove_texture
ObjectInWorld.new_texture=new_texture
ObjectInWorld.add_to_texture=add_to_texture
ObjectInWorld.get_textures=_get_textures
ObjectInWorld.light_level=_light_level
ObjectInWorld.rgbed=_rgbed
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


 
