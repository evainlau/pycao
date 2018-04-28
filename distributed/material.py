
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
        import povrayshoot
        string="matrix "+povrayshoot.povrayMatrix(mape)
        #
        return self.enhance(string,name)
        
        
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
    def __init__(self,string="",name=""):
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 
        self.largeString=self.__class__.__name__.lower()+" {"+self.smallString+"}"
        self.name=name
        if self.name:
            self.declareString="#declare "+self.name+" = "+self.largeString
            globvars.TextureString+="\n"+self.declareString

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
        if isinstance(listeOrItem,list):
            for entry in listeOrItem:
                self.enhance(entry,name="")
            if name:
                self.name=name
                self.declareString="#declare "+self.name+" = "+self.largeString
                globvars.TextureString+="\n"+self.declareString
        elif isinstance(listeOrItem,str):
            wc=len(listeOrItem.split())
            if wc>1:
                outstring=self.smallString+" "+listeOrItem
                #print("oui avec",outstring)
                self.__init__(outstring,name)
            else: # the item is a keyword, need to declare selfto add the item if not done already
                keyword=listeOrItem
                if not self.name:
                    self.name="Id"+str(id(self))
                    self.declareString="#declare "+self.name+" = "+self.largeString
                    globvars.TextureString+="\n"+self.declareString
                outstring=self.name+" "+keyword
                self.__init__(outstring,name)
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
        import povrayshoot
        string="matrix "+povrayshoot.povrayMatrix(mape)
        return self.enhance(string,name)

    def copy(self):#no deepcopy needed since contains only strings
        return copy.copy(self)    

def unleash(liste):
    texture=liste[0].texture
    for obj in liste:
        if not obj.texture==texture:
            raise NameError("All objects must share the same texture to unleash it")
    newtexture=texture.copy()
    for obj in liste:
        obj.makeup(newtexture)

def _makeup(self,texture):
    if isinstance(texture,str):#then should be a povray name texture
        import material
        texture=material.Texture(texture)
    self.texture=texture
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                _makeup(slave,texture)
    return self

def _enhance(self,value,name=""):
    self.texture.enhance(value,name)
    if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
        for op in self.csgOperations:
            slaves=op.csgSlaves
            for slave  in slaves :
                if not slave.texture==self.texture:#otherwise already done
                    _enhance(slave,value,name=name)
    return self


ObjectInWorld.makeup=_makeup
ObjectInWorld.enhance=_enhance

        
        
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

"""TO DO

Verifier la possibilit\'e de faire un carrelage et la Brick normale sur la porte !
remplacer makeup par painted_by
"""