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




    def move(self,map=None):
        """ This is the fundamental method to move any object : the user defines a map M  
        using any of the possible primitives in the class Map. Then self.move(M) 
        moves the object and all its children using the matrix M. Of course, for 
        very common displacements, there are primitives which encapsulates the computation 
        of the matrix and the call to move in a unique funcition : see for instance
        rotate,scale or translate, which use this principle. 
        """
        #print("move")
        #print(self)
        #print(map)
        self.move_alone(map)
        #print(self)
        #print("fin move")
        #print(self)
        for c in self.children:
            c.move(map)
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
        parent.children.append(self)
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


    def amputed_by(self,cuttingShape,throwShapeAway=True):
        """
        cut self using the substraction of cuttingShape, where cuttingShape=object or listOfObjects
        The cuttingShape is made invisible after the cutting operation if throwShapeAway=True
        """
        # I make a copy so that I can move the cutting shape independently of self later on
        #print("type")
        #print(type(cuttingShape))
        if isinstance(cuttingShape,list):
            #print("yes liste")
            #print(cuttingShape)
            copie=[tool.copy() for tool in cuttingShape]
        else:
            copie=[cuttingShape.copy()]
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


    def intersected_by(self,cuttingShape,throwShapeAway=True):
        """
        cut self using the intersection with cuttingShape
        The cuttingShape is made invisible after the cutting operation if throwShapeAway=True
        """
       # I make a copy so that I can move the cutting shape independently of self later on 
        if isinstance(cuttingShape,list):
           #print(cuttingShape)
           #print(type(cuttingShape[0]))
            copie=[copy.deepcopy(tool) for tool in cuttingShape]
           #print([tool.children for tool in cuttingShape])
           #print([tool.children for tool in copie])
           #print(self.visibility)
        else:
            copie=[cuttingShape.copy()]
        #print(cuttingShape)
        #print(copie)
        #print("mat",copie.materials,cuttingShape.materials)
        [tool.make_invisible() for tool in copie]
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


    def drill(self,diameter=None,segment=None):
        cylPercage=Cylinder(length=10*self.dim,radius=diameter/2.)
        direction=holeDirection
        map=matrix_for_parallelism(start=Z,end=direction)
        cylPercage.move(map)
        vec1=promote_to_vector(cylPercage,"ooo")
        vec2=promote_to_vector(self,handleOnAxis)
        cylPercage.translate(vector= vec2 - vec1)
        return self.amputed_by(cylPercage,throwShapeAway=True)

    def colored(self,color):
        self.color=color
        return self




class BoundedByBox(ObjectInWorld):
    """
    A class for objects with a box marker 
    """
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

    def move_against(self,other, selfFace1,otherFace1,selfFace2,otherFace2,offset=(0,0,0),adjustEdges=None,adjustAxis=None):
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
        M=selfBox._map_for_parallelism(otherBox,selfFace1,otherFace1,selfFace2,otherFace2)
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




