
PNFTString=""

class PNFItem(object)
    def __init__(self,string,name=""):
        "Builds a instance from the given string. Computes a name if the name option is not filled"
        if name:
            self.name=name
        else:
            self.name="Id"+str(id(self))
        self.smallString=string # the 'small' povray string ie. without the surrounding Pigment{} or Normal{} or Finish{} or Texture{} 
        self.largeString=self.__class__.__name__+" {"+self.smallString+"}"
        self.declareString="#declare "+self.name+" = "+self.largeString
        PNFTString+="\n"+self.declareString
            
    def enhance(self,stringOrPNFItem,newname=""):
        """
        takes a copy of self, adds the stringOrPNFItem options, and returns the modified copy
        This may be used to add diffuse or ambient options in a finish, or a transformation in a pigment,normal, etc... 
        """
        built=self.__class__.__new__()
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

    def move(self,map):
        raise NameError("Move is not yet implemented for PNFItems")
        
class Pigment(PNFItem):
    def __init__(self,*args,**kwargs):
        super().__init__(self,*args,**kwargs)
    
class Normal(PNFItem):
    def __init__(self,*args,**kwargs):
        super().__init__(self,*args,**kwargs)

class Finish(PNFItem):
    def __init__(self,*args,**kwargs):
        super().__init__(self,*args,**kwargs)


class Texture(object):
    @staticmethod
    def fromList(pnflist,name=""):
        """ in the list, there should be at most one Texture instance. The list is reorded so that string instances go to the end 
        to be consistent with povray Texture syntax """
        built=Texture()
        if not name:
            name="Id"+str(id(built))
        begin=""
        end=""
        middle=""
        for entry in pnflist:
            if isinstance(entry,str): #should be a PNF Item short long string
                end=end+" "+entry
            elif isinstance(entry,Texture): # the only texture, at the beginning
                begin=entry.name+" "
            elif isinstance(entry,Pigment) or isinstance(entry,Normal) or isinstance(entry,Finish):
                middle=middle+" "+entry.name
            else: 
                raise NameError("The entry in the list is neither a Texture,Pigment,a Normal nor a Finish")
        outstring=begin+" "+middle+" "+end
        PNFItem.__init__(built,outstring,name)
        PNFTString+="\n"+self.declareString


    def enhance(self,liste,newname=""):   
        newlist=[self]+liste
        return Texture.fromList(newlist,name=newname)
                
"""TO DO
jouer et verifier que PNFT string donne la chaine attendue
dans povrayshoot, ajouter PNFTString
appliquer des move 
attacher une structure par son nom (recursivement)
.colored prend la Texture et lui ajoute un pigment:texture.enhance([Pigment("color Red")])
ou cree la structure si non existante.
Verifier la possibilit\'e de faire un carrelage et la Brick normale sur la porte !
Nettoyer les essais infructueux
"""
