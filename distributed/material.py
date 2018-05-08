
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


class PNFItem(object):#PNF means Pigment,Normal or Finish
    def __init__(self,string,name=""):
        "Builds a instance from the given string. Computes a name if the name option is not filled"
        global globvars
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 
        self.largeString=self.__class__.__name__.lower()+" {"+self.smallString+"}"
        if name:
            self.name=name
            self.declareString="#declare "+self.name+" = "+self.largeString
            globvars.TextureString+="\n"+self.declareString
        else:
            self.name=""

            
        
    def enhance(self,stringOrPNFItem,newname=""):
        """
        takes a copy of self, adds the stringOrPNFItem options, and returns the modified copy
        This may be used to add diffuse or ambient options in a finish, or a transformation in a pigment,normal, etc... 
        """
        def _tostring(a):
            if isinstance(a,str):
                return a
            else:
                return a.smallString
        stringToAdd=_tostring(stringOrPNFItem)
        outstring=self.smallString +" "+stringToAdd
        self.__init__(outstring,newname)
        return self

    def move(self,mape,name=""):
        self.moveMap=mape*self.moveMap
        return self
        
        
class Pigment(PNFItem):
    def __init__(self,string,name=""):
        super(Pigment,self).__init__(string,name=name)
    
class Normal(PNFItem):
    def __init__(self,string,name=""):
        super().__init__(self,string,name=name)

class Finish(PNFItem):
    def __init__(self,string,name=""):
        super().__init__(self,string,name=name)


class Texture(object):
    def __init__(self,string="",name="",moveMap=None):
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 
        self.largeString=self.__class__.__name__.lower()+" {"+self.smallString+"}"
        self.name=name
        if self.name:
            self.declareString="#declare "+self.name+" = "+self.largeString
            globvars.TextureString+="\n"+self.declareString
        if moveMap is None:
            self.moveMap=Map.identity
            
    def __str__(self):
        import povrayshoot
        return povrayshoot.texture_string_cameraless(self)

    @staticmethod
    def from_colorkw(ckw):
        return Texture("pigment {color "+ckw+"}")

            
    @staticmethod
    def from_list(pnflist,name=""):
        """ in the list, there should be at most one Texture instance. The list is reorded so that string instances go to the end 
        to be consistent with povray Texture syntax """
        built=Texture.__new__(Texture)
        if not name:
            name="Id"+str(id(built))
        begin=""
        end=""
        middle=""
        for entry in pnflist:
            if isinstance(entry,str): #should be a PNF Item short long string or a transform map
                end=end+" "+entry
            elif isinstance(entry,Texture): # the only texture, at the beginning
                begin=entry.name+" "
            elif isinstance(entry,Pigment) or isinstance(entry,Normal) or isinstance(entry,Finish):
                middle=middle+" "+entry.name
            else: 
                raise NameError("The entry in the list is neither a Texture,Pigment,a Normal nor a Finish")
        outstring=begin+" "+middle+" "+end
        built.__init__(outstring,name)
        return built


    def enhance(self,listeOrItem,name=""):
        import povrayshoot
        if isinstance(listeOrItem,list):
            for entry in listeOrItem:
                self.enhance(entry,name="")
            if name:
                self.name=name
                self.declareString="#declare "+self.name+" = "+povrayshoot.texture_string_cameraless(self)
                globvars.TextureString+="\n"+self.declareString
        elif isinstance(listeOrItem,str):
            wc=len(listeOrItem.split())
            if wc>1:
                outstring=self.smallString+" "+listeOrItem
                #print("oui avec",outstring)
                self.__init__(outstring,name,moveMap=self.moveMap)
            else: # the item is a keyword, need to declare selfto add the item if not done already
                keyword=listeOrItem
                if not self.name:
                    self.name="Id"+str(id(self))
                    self.declareString="#declare "+self.name+" = "+self.largeString
                    globvars.TextureString+="\n"+self.declareString
                outstring=self.name+" "+keyword
                self.__init__(outstring,name,self.moveMap)
        elif isinstance(listeOrItem,PNFItem):
            if listeOrItem.name:
                self.enhance(listeOrItem.name,name)
            else:
                self.enhance(listeOrItem.largeString,name)
        else:
            print (type(listeOrItem),listeOrItem)
            raise NameError("The Texture should be enhances with a list,a PNF item, or a string")
        return self

    def move(self,mape,name=""):
        self.moveMap=mape*self.moveMap
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

def _add_to_texture(self,value,name=""):
    self.texture.enhance(value,name)
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                if not slave.texture==self.texture:#otherwise already done
                    _add_to_texture(slave,value,name=name)
    return self


def _get_textures(self,textureset=None,withChildren=True):
    if textureset is None:
        textureset=set()
    try:
        textureset.add(self.texture)
    except: # no texture
        pass
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                pass
                textureset.add(slave.texture)
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
        
def defaultTexture():
    return Texture("pigment {Yellow}")


