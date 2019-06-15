"""
    This is Pycao, a modeler and raytracer interpreter for 3D drawings
    Copyright (C) 2015  Laurent Evain

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""



import copy
from uservariables import *



# class Dico2Attribut(dict):
#     """" transforme un dictionnaire foo en un objet foo
#     dont les donnees sont accessibles par foo.bar en
#     plus de l'usuel  foo["bar"]
#     """
#     def __init__(self, *args, **kwargs):
#         super(Dico2Attribut, self).__init__(*args, **kwargs)
#         self.__dict__ = self


# the list of people included if filmAllActors==True
groupPhoto=[]

class Object(object):
    pass

class Scene(Object):
    "An object with a unique instance globVars to store the global variables of the scene"
    def __init__(self):
        self.TextureString=""

globvars=Scene()
globvars.userDefinedFunctions=""

class ObjectInWorld(object):
    """
    A class for all objects which are located in a 3-dimensional space, thus can be translated,rotated....   
    An  objectInWorld comes with a list self.children whose elements are instances of ObjectInWorld. In other words,
    an instance of ObjectInWorld is a tree. 
    init creates a tree without branches and there is a 
    method "self.transplantOn(otherObject) to populate the dictionnary. 
    The method move moves recursivly all the children with the parent. 

    Every object in World is insantiated with a attribute self.mapFromParts to indicate its position. 
    More precisely, to move an object with a map M, one can do self.mapFromParts=M*self.mapFromParts.
    This is a low level function in principle not used by the end user as this is wrapped 
    in the method move, which takes care of the children and other details. 
    An other warning : 
    Three coefficients of mapFromParts (namely those with index 0:2,3) indicate most of the time the position
    of the object, which means usually the center of gravity of the object.
    But it is advised not to try to interpret the coeffs as they  have no 
    clear meaning. Indeed  there are several ways to create
    the same object, this results in different matrices for the same object.
    A sphere with radius r can be created directly with a primitive
    so that mapFromParts=identtity matrix. But it can be the result of the dilatation 
    of a sphere of radius 1 with scale r, in which case mapFromParts=r.Identity.

    Attributes
    self.make_invisible() : self becomes invisible but still present for interactions (intersection,difference...)
    self.disappears() : self is not visible and not interacts neither
    self.glued_on(parent): self follow the parent in its movement
    self.annotates(parent): use self as marker for parent, ie. self is transplanted on parent to be usable for computations, but disappears
    self.move(map)
    self.amputed_by(self,cuttingShape,throwShapeAway=False): substract cuttingShape from self, the cuttingShape becomes invisible after operation if throwShapeAway=True
    self.drill(diameter,axis):


    """

# The  following methods 
#
#          translate,rotate,scale,__init__,is_vector,is_point 
#
#require mathutils so they are defined at the end of mathutils 
# to avoid cross depencies. 




    def __str__(self,recursive=False):
        string="Object In World "
        try:
            string+=str(self.name)
        except:
            pass
        string += "\nMatrix: "+str(self.mapFromParts)
        try:
            string+="Parent:"+ str(self.parent.name)
        except:
            pass
        return ( string )


    def named(self,str):
        self.name=str
        return self

    def move(self,map=None,topLevel=True):
        """ This is the fundamental method to move any object : the user defines a map M  
        using any of the possible primitives in the class Map. Then self.move(M) 
        moves the object and all its children using the matrix M. Of course, for 
        very common displacements, there are primitives which encapsulates the computation 
        of the matrix and the call to move in a unique funcition : see for instance
        rotate,scale or translate, which use this principle. 
        """
        #print("move",self.name)
        #print(map)
        self.move_alone(map)
        #print("Less enfants a bouger maintenant")
        #print([c.name for c in self.children])
        #print(self)
        #print("fin move")
        #print(self)
        #print("in move,generic")
        #print(self)
        for c in self.children:
            c.move(map,topLevel=False)
        import material
        if topLevel==True:
            textureset=self.get_textures()
            for tex in textureset:
                #pass
                tex.move(map)
        return self

    def descendants_and_myself(self):
        # The list of descendants of self, including self itself.
        descendants=[self]
        for child in self.children:
            descendants=descendants+child.descendants_and_myself()
        return descendants


    def glued_on(self,parent):
        """
        makes self follow the parent in its movements. 
        """
        self.parent=parent
        try:
            parent.children.append(self)
        except:
            if hasattr(parent,"children") :
                raise NameError('Erreur dans Glued  On')
            else :
                parent.children=[self]
        return self

    def remove_children(self):
        """
        """
        self.children=[]
        return self


    def annotates(self,parent):
        """
        use self as marker for parent, ie. self is transplanted on parent to be usable for computations, but disappears
        """
        self.parent=parent
        parent.children.append(self)
        self.disappears()

        
    def move_alone(self,matrix):
        raise NameError('Method to be overwritten for each objectInWorld')
        #self.mapFromParts=matrix*self.mapFromParts
        # this is the generic method to be rewritten for every object

    def make_invisible(self):
        """
        self.make_invisible makes the object invisible. However the 
        object still interacts with other objects, for intersection or difference.
        See self.disappears to totally remove the object
        """
        self.visibility=0
        #print("Les attributs")
        #print(self.__dict__)
        for c in self.children:
            #print(c.name)
            #print(c.__dict__)
            c.make_invisible()

    def remove_from_group_photo(self):
        groupPhoto.remove(self)
            
    def disappears(self):
        """
        self.disappears() makes the object disappear ie invisible and with no
        interaction with other objects, for intersection or difference.
        See self.make_invisible() to get an invisible object still present in interactions.
        """
        self.visibility=0
        self.booleanVisibility=0
        for c in self.children:
            c.make_invisible()


    def amputed_by(self,cuttingShape,throwShapeAway=True,keepTexture=True):
        """
        cut self using the substraction of cuttingShape, where cuttingShape=object or listOfObjects
        The cuttingShape is made invisible after the cutting operation if throwShapeAway=True
        """
        # I make a copy so that I can move the cutting shape independently of self later on
        #print("type")
        #print(type(cuttingShape))
        if not isinstance(cuttingShape,list):
            cuttingShape=[cuttingShape]
        if keepTexture and hasattr(self,"texture"):
            copie=[tool.copy().remove_texture() for tool in cuttingShape]
        else:
            copie=[tool.copy() for tool in cuttingShape]
        #print("mat",copie.materials,cuttingShape.materials)
        #print("Les outils de coupe")
        #print([tool.children for tool in copie])
        [tool.make_invisible() for tool in copie]
        [tool.glued_on(self) for tool in copie]# Then I can move self and the intersection remains OK 
        if throwShapeAway:
            if isinstance(cuttingShape,list):
                [tool.make_invisible() for tool in cuttingShape]
            else:
                cuttingShape.make_invisible()
        csgOperation=Object()
        csgOperation.csgKeyword="difference"
        csgOperation.csgSlaves=copie
        csgOperation.keepTexture=keepTexture
        self.csgOperations.append(csgOperation)
        return self

    def amputed_by2(self,cuttingShape,throwShapeAway=True,keepTexture=True):
        """
        cut self using the substraction of cuttingShape, where cuttingShape=object or listOfObjects
        The cuttingShape is made invisible after the cutting operation if throwShapeAway=True
        """
        # I make a copy so that I can move the cutting shape independently of self later on
        #print("type")
        #print(type(cuttingShape))
        if not isinstance(cuttingShape,list):
            cuttingShape=[cuttingShape]
        if keepTexture and hasattr(self,"texture"):
            copie=[tool.copy().new_texture(self.texture) for tool in cuttingShape]
        else:
            copie=[tool.copy() for tool in cuttingShape]
        #print("mat",copie.materials,cuttingShape.materials)
        #print("Les outils de coupe")
        #print([tool.children for tool in copie])
        [tool.make_invisible() for tool in copie]
        [tool.glued_on(self) for tool in copie]# Then I can move self and the intersection remains OK 
        if throwShapeAway:
            if isinstance(cuttingShape,list):
                [tool.make_invisible() for tool in cuttingShape]
            else:
                cuttingShape.make_invisible()
        csgOperation=Object()
        csgOperation.csgKeyword="difference"
        csgOperation.csgSlaves=copie
        self.csgOperations.append(csgOperation)
        return self

    def intersected_by(self,cuttingShape,throwShapeAway=True,keepTexture=True):
        """
        cut self using the intersection with cuttingShape
        The cuttingShape is made invisible after the cutting operation if throwShapeAway=True
        """
        # I make a copy so that I can move the cutting shape independently of self later on
        #print("in intersected by")
        if not isinstance(cuttingShape,list):
            cuttingShape=[cuttingShape]
           #print(cuttingShape)
           #print(type(cuttingShape[0]))
        copie=[]
        for tool in cuttingShape:
            memo=dict()
            theCopy=copy.deepcopy(tool,memo)
            if keepTexture and hasattr(self,"texture"):
                theCopy.new_texture(self.texture)
            #else:
            #    pass
                #print("Not TexturedAsSelf")
            copie.append(theCopy)
        #print("mat",copie.materials,cuttingShape.materials)
        [tool.make_invisible() for tool in copie]
        #comp=Compound()
        #comp.add_to_compound(self)
        #[comp.add_to_compound(tool) for tool in copie]# Then I can move self and the intersection remains OK
        #self=comp
        [tool.glued_on(self) for tool in copie]# Then I can move self and the intersection remains OK 
        if throwShapeAway:
            if isinstance(cuttingShape,list):
                [tool.make_invisible() for tool in cuttingShape]
            else:
                cuttingShape.make_invisible()
        csgOperation=Object()
        csgOperation.csgKeyword="intersection"
        csgOperation.csgSlaves=copie
        self.csgOperations.append(csgOperation)
        return self


    def drilled_by_cylinder(self,segment=None,radius=None):
        cylPercage=ICylinder(segment,radius)
        return self.amputed_by(cylPercage,throwShapeAway=True)

    # def colored(self,color):
    #     self.colored_alone(color)
    #     if hasattr(self,"csgOperations") and len(self.csgOperations)>0:
    #         for op in self.csgOperations:
    #             slaves=op.csgSlaves
    #             for slave  in slaves :
    #                 slave.colored(color)
    #     return self


    
# class BoundedByBox(ObjectInWorld):
#     """
#     A class for objects with a box marker 
#     """
    def point(self,*args,**kwargs):
        return self.box().point(*args,**kwargs)

    def segment(self,*args,**kwargs):
        return self.box().segment(*args,**kwargs)

    def plane(self,*args,**kwargs):
        return self.box().plane(*args,**kwargs)

    @property
    def dimensions(self):
        return self.box().dimensions
    @property
    def center(self):
        return self.box().point(0.5,0.5,0.5,"ppp")

    def against(self,other, selfFace1,otherFace1,selfFace2,otherFace2,offset=(0,0,0),adjustEdges=None,adjustAxis=None):
        """
        Moves self against other, using the faces of self.box() and other.box().
        More precisely, self is rotated such that selfFace1,selfFace2 are parallel respectivly to otherFace1,otherFace2.
        Then self is translated so that selfFace1 coincides with a face of other, and that the 2 faces have the same center.
        Finally self is translated again to adjust the position when the parameters
        offset,adjustEdges,adjustAxis are filled. 

        parameters:
        selfFace,otherFace: X,-X,Y,-Y,Z or -Z
        offset = (x,y,z) triple of floats or a vector
        adjustEdges=a vector aX+bY+cZ with a,b,c in [0,1,-1]
        adjustAxis=[markerOfSelf,markerOfOtherBox], where markers= a point or a line transversal to the common plane.

        To see what means parallellism for non orthogonal boxes, look _map_for_parallelism.
        For precise description of the offset, see _map_translate_against 
        """
        selfBox=self.box()
        otherBox=other.box()
        #print("in against,generic.py")
        #print(selfBox)
        #print(otherBox)
        try:
            M=selfBox._map_for_parallelism(otherBox,selfFace1,otherFace1,selfFace2,otherFace2)
        except:
            raise NameError("Non invertible matrix, probably got a box whose volume is zero")
            #I have to be careful here because the argument adjustAxis, may be a child of self or not.
        # Thus I make a copy so that I am sure this is not a child
        if adjustAxis is not None:
            selfAxisCopy=adjustAxis[0].copy()
            selfAxisCopy.move_alone(M)
            newAxis=[selfAxisCopy,adjustAxis[1]]
        else:
            newAxis=adjustAxis
        # same thing for adjust Edges
        #if adjustEdges is not None:
        #edgesCopy=adjustEdges.copy()
        #    edgesCopy.move_alone(M)
        #else:
        #    edgesCopy=adjustEdges

        self.move(M)
        selfBox=self.box()
        N=selfBox._map_translate_against(otherBox, faceOfSelf=selfFace1, offset=offset,adjustEdges=adjustEdges,adjustAxis=newAxis)
        #print('FIN MOVE')
        return(self.move(N))

        
    def screw_on(self,other,adjustAlong=None,adjustAround=None):
        """ 
        other=a Segment
        adjustAlong=[point1,point2]
        adjustAround=[point3,point4]
         Consider an isometry map M such that 
        - M(self).vector et otherAxis.vector are positivly proportional
        - M(self) et otherAxis have a point in common
        - M(point1)-point2 is orthogonal to otherAxis.vector
        -M(point3),point4 is a line coplanar to otherAxis and in the same half plane
        Then self is transformed to self.move(M) 
        """
        M=self.axis().screw_map(other,adjustAlong,adjustAround)
        self.move(M)
        return self

 
    def box(self,name=None): #will be overwritten for some objects construcing their own boxes
        if name is None:
            return self.activeBox.copy()
        else :return getattr(self.dicobox,name).copy()
    def axis(self,name=None): #will be overwritten for some objects construcing their own boxes
        if name is None:
            return self.activeAxis.copy()
        else: return getattr(self.dicoaxis,name).copy()
    def hook(self,name=None): #will be overwritten for some objects construcing their own boxes
        if name is None:
            return self.activeHook.copy()
        else: return getattr(self.dicohook,name).copy()

    
    def add_box(self,name,framebox):
        """
        Add a new box to self and select it. The box 
        is added to the dictionnary self.dicobox. 
        The activebox is self.box()
        """
        # the added box must move with the object
        # creates a dicobox if ncr and populates it if  ncr
        if not hasattr(self,"dicobox"):
            dicobox=Object() # The pair k,v with k a string and v a callable returning a framebox
            if hasattr(self,"box"):
                dicobox.initialBox=self.box
            setattr(self,"dicobox",dicobox)
        self.activeBox=framebox.copy().glued_on(self)
        setattr(self.dicobox,name,self.activeBox)
        return self



    
    def add_axis(self,name,line):
        """
        Add a new axis to self and select it. The line
        is added to the dictionnary self.dicoaxis. 
        The active axis is self.axis()
        """
        # the added line must move with the object
        def axis_function():
            return gluedLine
        # creates a dicoaxis if ncr and populates it if  ncr
        if not hasattr(self,"dicoaxis"):
            dicoaxis=Object() # The pair k,v with k a string and v a callable returning a line
            if hasattr(self,"axis"):
                dicoaxis.initialAxis=self.axis
            setattr(self,"dicoaxis",dicoaxis)
        self.activeAxis=line.copy().glued_on(self)
        setattr(self.dicoaxis,name,self.activeAxis)
        return self

    def add_hook(self,name,hpoint):
        """
        Add a new hook to self and select it. The point
        is added to the dictionnary self.dicohook
        The active hookpoint is self.hookpoint()
        """
        # creates a dicoaxis if ncr and populates it if  ncr
        if not hasattr(self,"dicohook"):
            dicohook=Object() 
            setattr(self,"dicohook",dicohook)
        self.activeHook=hpoint.copy().glued_on(self)
        setattr(self.dicohook,name,self.activeHook)
        return self

    
    def print_boxes(self):
        """
        displays the list of boxes of self
        """
        try:
            print ( self.dicobox.__dict__.keys())
        except:
            try:
                print(self.box())
                print("The above framebox is the  unique box")
            except:
                print("No box")
        return self
  
    def select_box(self,name):
        """ 
        arguments: 
        name: the name of the box we want to select
        """
        self.activeBox=getattr(self.dicobox,name)
        return self


    def print_axes(self):
        """
        displays the list of  axes of self
        """
        try:
            print ( self.dicoaxis.__dict__.keys())
        except:
            try:
                print(self.axis())
                print("The above axis is the  unique axis")
            except:
                print("No axis")
        return self
  
    def select_axis(self,name):
        """ 
        arguments: 
        name: the name of the axis we want to select
        """
        self.activeAxis=getattr(self.dicoaxis,name)
        return self

    def self_rotate(self,angle):
        return self.rotate(self.axis(),angle)

    def self_pirotate(self,angle):
        return self.rotate(self.axis(),math.pi*angle)

    def self_degrotate(self,angle):
        return self.rotate(self.axis(),math.pi*angle/90)

    
    def self_translate(self,amount,type="p"):
        if type=="p": vec=amount* self.axis().vector
        elif type=="a": vec=amount*self.axis().vector.normalized_copy()
        else: return NameError("Type should be a or p")
        return self.translate(vec)

    def self_gtranslate(self,goal,vec=None,start=None,):
        if start is None:
            start=self.hook()
        if vec is None:
            vec=self.axis().vector
        import mathutils
        if not mathutils.is_point(goal):
            goal=goal.hook()
        self.gtranslate(vec,start,goal)
        return self

    def print_hooks(self):
        """
        displays the list of  hooks of self
        """
        try:
            print ( self.dicohook.__dict__.keys())
            print ("are the hooks")
        except:
            try:
                print(self.hook())
                print("The above hook is the  unique hook")
            except:
                print("No hook")
        return self
  
    def select_hook(self,name):
        """ 
        arguments: 
        name: the name of the hook we want to select
        """
        self.activeHook=getattr(self.dicohook,name)
        return self

    def copy(self):
        memo=dict()
        return copy.deepcopy(self,memo)
