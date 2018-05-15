
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
* string Titems and PNF items : the smallstring which is a sting considered by povray without the pigment{..} or texture{...} 
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
- the context ( in a declaration string or nested within a surronding texture in povrayshoot ( unnestedstring et nestedstring) 
- the instance (PNF items have different rules than T items)
- if we want to include the displacement matrinx  or not in the  string ( withMove=True or False) 

___________________________________________________________________________________________________________________________________________
          |                                                        |                                                                     |
          |             unnamed                                    |                          named                                      |
__________________________________________________________________________________________________________________________________________
          |                                                        |                                                                     |
          |         pigment {smallstring moveString}               |                 pigment {name movestring}                           |
          |                                                        |                                                                     |
          |         texture {smallstring moveStrting} (stringy)    |                 texture {name movestring}                           |
unnnested                 
          |   texture{nestedOutput(t1)...} for t=[t1,...]          |               (A named texture is stringy, thus non recursive)      |
______________________________________________________________________________________________________________________________
          |                                                        |                                                                     |
          |           pigment { smallstring movestring}            |                     pigment {name movestring}                       |
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

################
Implementation details
################
To homonegeize the code for stringy and recursive textures, the class Texture derives from list and 
for a stringy instance, we init by i.append(i). This sounds strange but this is very efficient, 
as it gives a perfect identification between i and [i]. 

"""


class PNFTItem(object):#PNF means Pigment,Normal or Finish or texture
            
    def named(self,name,withMove=False):
        self.name=name
        nameDeclared=self.name
        if withMove:
            nameDeclared+="WithMove"
        globvars.TextureString+="\n#declare "+nameDeclared+" = "+self.declaration_string(withMove=withMove)
        self.smallString=self.name
        if isinstance(self,Texture):
            self.stringy=True 
        return self

    def declaration_string_bracketless(self,withMove=False):
        string=self.__class__.__name__.lower()+" {"+self.get_smallString(withMove=withMove)
        if withMove and hasattr(self,"moveMap"):
            import povrayshoot
            string+=" matrix "+povrayshoot.povrayMatrix(self.moveMap)
        return  string

    
    def declaration_string(self,withMove=False):
        return  self.declaration_string_bracketless(withMove=withMove)+"}"

    def __str__(self):
        return  self.declaration_string(withMove=True)

class PNFItem(PNFTItem):#PNF means Pigment,Normal or Finish
    def __init__(self,string):
        "Builds a instance from the given string. Computes a name if the name option is not filled"
        global globvars
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 

    def get_smallString(self,withMove=False):
        ret=self.smallString
        if withMove and hasattr(self,"moveMap"):
            import povrayshoot
            ret+=" matrix "+povrayshoot.povrayMatrix(self.moveMap)
        return ret

    def get_reducedString(self,withMove):
        return self.declaration_string(withMove)
        
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
    
class Normal(PNFItem):
    def __init__(self,string):
        super(Normal,self).__init__(string)

class Finish(PNFItem):
    def __init__(self,string):
        super(Finish,self).__init__(string)


class Texture(PNFTItem,list):

    def get_smallString(self,withMove=False):# seems that it is always called with withMove=True in practice. Argument useful for PNF but not T-items ?
        # The first item may be a named texture
        return " ".join([entry.get_reducedString(withMove=withMove) for entry in self])

    


    def move(self,mape):
        if self.stringy: # defined by a string, no recursion occurs
            try:
                self.moveMap=mape*self.moveMap
            except: #probably not moved yet and no movemap defined
                self.moveMap=mape
            return self
        else:
            [entry.move(mape) for entry in self]

    def __new__(cls,*args,**kwargs):
        return list.__new__(cls)
            
    def __init__(self,*args):
        if len(args)==1 and isinstance(args[0],str):
            self.stringy=True #?? not used it seems
            print("les args")
            for l in args:
                print(l )
            print("fin")
            self.smallString=args[0] # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{}
            def sms(withMove=False):
                """ This function computes a string which is a valid for the declared texture
                builds a name declares and declares the string with the identifier name. 
                then returns the name
                """
                idName="IdAuto"+str(id(self))
                if withMove and hasattr(self,"moveMap"):
                    import povrayshoot
                    moveString=" matrix "+povrayshoot.povrayMatrix(self.moveMap)
                else: moveString=" "
                declareString="\n#declare " +idName +" = texture{"+self.smallString+ moveString+"}\n"
                print("la declare string pour l'entree ", args[0],"est", declareString)
                globvars.TextureString+=declareString
                return idName
            self.get_reducedString=sms
            self.append(self)
        else:
            self.stringy=False
            for entry in args:
                self.append(entry)


    @staticmethod
    def from_colorkw(ckw):
        return Texture("pigment {color "+ckw+"}")

            
#     @staticmethod
#     def from_list(pnflist,name=""):
#         """ in the list, there should be at most one Texture instance. The list is reorded so that string instances go to the end 
#         to be consistent with povray Texture syntax """
#         built=Texture.__new__(Texture)
#         if not name:
#             name="Id"+str(id(built))
#         begin=""
#         end=""
#         middle=""
#         for entry in pnflist:
#             if isinstance(entry,str): #should be a PNF Item short long string or a transform map
#                 end=end+" "+entry
#             elif isinstance(entry,Texture): # the only texture, at the beginning
#                 begin=entry.name+" "
#             elif isinstance(entry,Pigment) or isinstance(entry,Normal) or isinstance(entry,Finish):
#                 middle=middle+" "+entry.name
#             else: 
#                 raise NameError("The entry in the list is neither a Texture,Pigment,a Normal nor a Finish")
#         outstring=begin+" "+middle+" "+end
#         built.__init__(outstring,name)
#         return built
# ;



    def enhance(self,listeOrItem):
        import povrayshoot
        if isinstance(listeOrItem,list):
            for entry in listeOrItem:
                self.enhance(entry)
        elif isinstance(listeOrItem,PNFItem):
            try:
                self.append(listeOrItem)
            except: #probably no texture yet
                self.texture=Texture(listeOrItem)
        else:
            print (type(listeOrItem),listeOrItem)
            raise NameError("The Texture should be enhances with a list,a PNF item, or a string")
        return self

    def copy(self):#no deepcopy needed since contains only strings
        memo=dict()
        return copy.deepcopy(self,memo)    



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


def _get_textures(self,textureset=None,withChildren=True):
    if textureset is None:
        textureset=[]
    try:
        textureset.append(self.texture)
        pass
    except: # no texture
        pass
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                toAdd=slave.get_textures()
                for entry in toAdd:
                    if id(entry) not in [id(entry) for entry in textureset]:#id necessary to avoid infinite loop
                        textureset.append(entry)
                #except: pass # notexture for the slave
    if withChildren:
        for c in self.children:
            c.get_textures(textureset=textureset)
    return textureset
    
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


oakPlanarTexture1="texture{pigment {image_map {png \"chene.png\"  }} rotate -90*y } ," #the grain is along Y
oakPlanarTexture2="texture{pigment {image_map {png \"chene.png\"  }} rotate -90*x } ," #the grain is along Y
oakPlanarTexture3="texture{pigment {image_map {png \"chene.png\"  }}  } ," #the grain is along Y
colorTexture="texture{ pigment{color rgb<1.0 , 0.4, 0.0>}}"
#oakPlanarPigment=" color rgb<1.0, 0.0, 0.0>," 
oakCubicTexture=Texture("cubic "+ oakPlanarTexture1 + oakPlanarTexture2 + oakPlanarTexture3+oakPlanarTexture1+oakPlanarTexture2+oakPlanarTexture3).named("cubicOak")
oakCylindricalTexture=Texture("pigment {image_map {png \"chene.png\" map_type 2 }}")
oakTexture=Texture("pigment {image_map {png \"chene.png\" }}")
wengeTexture=Texture("pigment {image_map {png \"wenge.png\" }}")
