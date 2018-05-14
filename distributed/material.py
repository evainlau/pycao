
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
Here I want,pigment,normals and finishes and textures,
pigments and normals and finishes have a  move map. 
some textures like the cubic one, don't support finishes 
or movemaps so they should be encapsulated in a name.
Une entite nommee est automatically declared in povray. 
 
The input of pigment is 
a pigment smallstring, the smallstring may contain previously named pigments or povray names. The smallstring by
def does not containt the "pigment{}" surrounding neither the movemap 
Similar  for normal. 

The input of a texture instance is a string as for pnf items, or a list where each element 
of the list is:
a pnf or texture instance. As for the input, if this is a pnf item, ok recognized by the language. 
if one of the items input is a word, it is a povray string and the povrayshoot output will be "texture{povrayname matrix}"
for that texture. Idem si c'est une string plus longue, l'output will be "texture{longerString matrix}. Thus these 
input strings correspond to special textures with an attribute smallString. Moving a structure moves each element in the list. 
The output string is the concatenation of the output strings of each element in the list ( this is a recursive procedure 
since textures contains textures). Thus there is a callable "smallstring" attached to each texture. This is generic but 
overwritten for textures imput by strings. In contrast smallstring is an attribute, not a callable for pnf items. 

longstrings are defined similarly for pnft items as classname+{+shortstring + moveMap}
When a pnft item has been named, its shortstring is equal to its name. To enhance, we enhance the shortstring
for pnf items and we add an element to the list in the case of textures. 

"""


class PNFTItem(object):#PNF means Pigment,Normal or Finish or texture
            
    def named(self,name):
        self.name=name
        globvars.TextureString+="\n#declare "+self.name+" = "+self.declaration_string()
        self.smallString=self.name
        if isinstance(self,Texture):
            self.stringy=True 
        return self

    def declaration_string_bracketless(self):
        return  self.__class__.__name__.lower()+" {"+self.get_smallString()

    
    def declaration_string(self):
        return  self.declaration_string_bracketless()+"}"

    

class PNFItem(object):#PNF means Pigment,Normal or Finish
    def __init__(self,string):
        "Builds a instance from the given string. Computes a name if the name option is not filled"
        global globvars
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 

    def get_smallString(self):
        return self.smallString
        
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
        if isinstance(self,"Finish"):
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

    def get_smallString(self):
        return " ".join([entry.get_smallString() for entry in self])


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
            self.stringy=True
            self.smallString=args[0] # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{}
            def sms():
                return self.smallString
            self.get_smallString=sms
        else:
            self.stringy=False
            # param should be a sequence of pnft items
            for entry in args:
                if not isinstance(entry,str):
                    self.append(entry)
                else:
                    self.append(Texture(entry)) 

            
    def __str__(self):
        import povrayshoot
        return povrayshoot.texture_string_cameraless(self)

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
                    if entry not in textureset:
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
