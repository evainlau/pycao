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


class PNFItem(object):
    def __init__(self,string,name=""):
        "Builds a instance from the given string. Computes a name if the name option is not filled"
        global globVars
        if name:
            self.name=name
        else:
            self.name="Id"+str(id(self))
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 
        self.largeString=self.__class__.__name__.lower()+" {"+self.smallString+"}"
        self.declareString="#declare "+self.name+" = "+self.largeString
        globVars.TextureString+="\n"+self.declareString

        
    def enhance(self,stringOrPNFItem,newname=""):
        """
        takes a copy of self, adds the stringOrPNFItem options, and returns the modified copy
        This may be used to add diffuse or ambient options in a finish, or a transformation in a pigment,normal, etc... 
        """
        built=self.__class__.__new__(self.__class__)
        if not newname:
            newname="Id"+str(id(built))
        def _tostring(a):
            if isinstance(a,str):
                return a
            else:
                return a.smallString
        stringToAdd=_tostring(stringOrPNFItem)
        outstring=self.name+" "+stringToAdd
        built.__init__(outstring,newname)
        return built

    def move(self,mape,name=""):
        import povrayshoot
        string="matrix "+povrayshoot.povrayMatrix(mape)
        return self.enhance(string,name)
        
        
class Pigment(PNFItem):
    def __init__(self,*args,**kwargs):
        super(Pigment,self).__init__(*args,**kwargs)
    
class Normal(PNFItem):
    def __init__(self,*args,**kwargs):
        super().__init__(self,*args,**kwargs)

class Finish(PNFItem):
    def __init__(self,*args,**kwargs):
        super().__init__(self,*args,**kwargs)


class Texture(object):
    def __init__(self,string="",name="",declare=True):
        if name:
            self.name=name
        else:
            self.name="Id"+str(id(self))
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 
        self.largeString=self.__class__.__name__.lower()+" {"+self.smallString+"}"
        if declare:
            self.declareString="#declare "+self.name+" = "+self.largeString
            globVars.TextureString+="\n"+self.declareString
        
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
            newlist=[self]+listeOrItem
        elif isinstance(listeOrItem,str) or isinstance(listeOrItem,PNFItem):
            newlist=[self,listeOrItem]
        else:
            print (type(listeOrItem),listeOrItem)
            raise NameError("The Texture should be enhances with a list,a PNF item, or a string")
        return Texture.from_list(newlist,name=name)

    
    def move(self,mape,name=""):
        import povrayshoot
        string="matrix "+povrayshoot.povrayMatrix(mape)
        return self.enhance(string,name)

yellowTexture=Texture.from_list([Pigment("Yellow",name="YellowPigment")],name="YellowTexture")

"""TO DO

.colored prend la Texture et lui ajoute un pigment:texture.enhance([Pigment("color Red")])
ou cree la structure si non existante.
Verifier la possibilit\'e de faire un carrelage et la Brick normale sur la porte !
Nettoyer les essais infructueux
"""
