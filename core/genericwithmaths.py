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

import numpy as np
#import bpy
import math
import sys,os
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac

from uservariables import *
from generic import *
from mathutils import *
from aliases import *
#import aliases
from elaborate import ICylinder
import material
import lights
################################################################
"""
                Adding some elements in the class ObjectInWorld
                possible now that we have math objects
"""
################################################################



def _translate_object(self,*args):
    #print(Map.translation(*args)*Map.identity)
    #print ("dans translate")
    #print (self)
    #for child in self.children:
    #    print(child)
    self.move(Map.translation(*args))
    #print(self)
    #for child in self.children:
    #    print(child)
    #import povrayshoot
    #import cameras
    #print(povrayshoot.object_string_recursive(self,cameras.Camera()))
    return self

def _gtranslate_object(self,vec,p1,p2):
    """
    translates self along a translation t with vector v such that  t(p1),p2 are in a common plane orthogonal to v
    """
    w=vec.clone().normalize()
    if is_point(p1):
        start=p1
    else:
        start=p1.hook()
    if is_point(p2):
        end=p2
    else:
        end=p2.hook()
    delta=(end-start).dot(w)
    self.translate(delta*w)
    return self



def _rotate_object(self,axis,angle):
    self.move(Map.rotation(axis,angle))
    return self

def _pirotate_object(self,axis,angle):
    self.rotate(axis,math.pi*angle)
    return self


def _scale_object(self,fx=1,fy=1,fz=1,xVector=X,yVector=Y, zVector=Z,fixedPoint=T):
    self.move(Map.scale(fx=fx,fy=fy,fz=fz,xVector=xVector,
                        yVector=yVector, zVector=zVector,fixedPoint=fixedPoint))
    return self

def _parallel_to(self,other,fixed=None):
    if  is_vector(other):
        goal=other
    elif hasattr(other,"axis"):
        goal=other.axis().vector
    elif hasattr(other,vector):
        goal=other.vector
    else: raise nameError("other should be a vector, a segment, or an object with an axis")
    if is_vector(self):
        start=self
    elif hasattr(self,"axis"):
        start=self.axis().vector
    elif hasattr(self,vector):
        start=vector
    else: raise nameError("self should be a vector, a segment, or an object with an axis")
    M=Map.rotational_difference(start,goal)
    if fixed is not None:
        myVec=fixed-point(0,0,0)
        N=Map.translation(myVec)
        P=Map.translation(-myVec)
        M=N*M*P
    self.move(M)
    return self

def _grotate(self,ax,o1,o2):
    if isinstance(ax,Segment):
        rotaxis=ax
    else:
        rotaxis=ax.axis()
    if  is_point(o1):
        p1=o1
    elif hasattr(o1,"hook"):
        p1=o1.hook()
    else: raise nameError("o1 should be a point or an object with a hook")
    if  is_point(o2):
        p2=o2
    elif hasattr(o1,"hook"):
        p2=o2.hook()
    else: raise nameError("o2 should be a point or an object with a hook")
    vec1=(p1-rotaxis.p1).cross(rotaxis.vector)
    vec2=(p2-rotaxis.p1).cross(rotaxis.vector)
    #print(vec1,vec1.__class__)
    #print(vec2,vec2.__class__)
    #print(o2)
    angle=vec1.angle_to(vec2,rotaxis.vector)
    #print("L angle est ", angle)
    M=Map.rotation(rotaxis,angle)
    self.move(M)
    return self
    
def _self_grotate(self,o2):
    return self.grotate(self.axis(),self.hook(),o2)


def flipXY(self):
    return self.move(Map.linear(Y,X,Z))

def flipXZ(self):
    return self.move(Map.linear(Z,Y,X))

def flipYZ(self):
    return self.move(Map.linear(X,Z,Y))

def flipX(self):
    return self.move(Map.linear(-X,Y,Z))

def flipY(self):
    return self.move(Map.linear(X,-Y,Z))

def flipZ(self):
    return self.move(Map.linear(X,Y,-Z))





@staticmethod
def _new_object(cls,*args,**kwargs):
    #dico={hook.name:hook for hook in hooks}
    self=super(ObjectInWorld,cls).__new__(cls)
    ObjectInWorld.__init__(self,args,kwargs) # on multiple inheritance, __new__ is not called so some empty initialisation that should be in __new__ are deported to __init__(self,...)
    # The other alternative would be to rewrite differently the __new__ passing self as an argument to some of them. It would be more coherent as we really create an "empty" object. However, this
    # would interfere badly with the copy.deepcopy() which calls __new__ with no arguments usually. 
    return self

def _init_object(self,*args,**kwargs):
    " put groupPhoto=False for not adding to groupPhoto"
    keys = sorted(kwargs.keys())
    if "name" in keys:
        self.name=kwargs["name"]
#    self.materials=[]
#    if "material" in keys:
#        self.materials.append(kwargs["material"])
#    else:
#        self.materials.append(DEFAULT_COLOR)
    self.mapFromParts=Map.identity()
    if "booleanVisibility" in keys:
        self.visibility=kwargs["visibility"]
    else:
        self.visibility=1
    if "booleanVisibility" in keys:
        self.booleanVisibility=kwargs["booleanVisibility"]
    else:
        self.booleanVisibility=1
    #print("dans Init")
    self.children=[]
    self.parent=[]
    #from material import Texture
    self.csgOperations=[]
    #print (allObjects)
    #print(self)
    # Adding, with no checking, duplicates remove when rendering
    if  ((isinstance(self,ObjectInWorld) and not isinstance(self,Primitive) and not isinstance(self,material.PNFTItem) and not isinstance(self,lights.Light)) \
         or isinstance(self,AffinePlane) \
         or isinstance(self, ParametrizedCurve)):
        groupPhoto.append(self)
    #   not isinstance(self,MassPoint):

ObjectInWorld.translate=_translate_object
ObjectInWorld.gtranslate=_gtranslate_object
ObjectInWorld.rotate=_rotate_object
ObjectInWorld.grotate=_grotate
ObjectInWorld.self_grotate=_self_grotate
ObjectInWorld.pirotate=_pirotate_object
ObjectInWorld.scale=_scale_object
ObjectInWorld.__init__=_init_object
ObjectInWorld.__new__=_new_object
ObjectInWorld.flipZ=flipZ
ObjectInWorld.flipY=flipY
ObjectInWorld.flipX=flipX
ObjectInWorld.flipXY=flipXY
ObjectInWorld.flipXZ=flipXZ
ObjectInWorld.flipYZ=flipYZ
#object.is_vector=is_vector_object
#object.is_point=is_point_object

#print (vector)

def _hooked_on(self,other):
    """ other,self=an abject with a hook, move self so that self.hook() and other.hook()  coincide. 
    If other is a point, self.hook goes to this point."""
    if is_point(other):
        self.translate(other-self.hook())
    else:
        self.translate(other.hook()-self.hook())
    return self


def _move_at(self,*location):
    # HIGHLY deprecated. DO NOT USE PLEASE. ADD A hook and use _hooke_on
    from aliases import point
    #print(len(location))
    #print(location)
    if len(location)==3:
        location=point(*location)
    else:
        location=location[0]
    #print(location)
    #print(self.center)
    vector=location-self.center
    return self.translate(vector)


def _move_below(self,other, offset=(0,0,0),adjustEdges=None,adjustAxis=None):
    if is_point(other):
        return self.translate(other-self.point(.5,.5,1,"ppp"))
    else:
        return self.against(other,Z,Z,X,X,offset,adjustEdges,adjustAxis)

def _move_above(self,other, offset=(0,0,0),adjustEdges=None,adjustAxis=None):
    if is_point(other):
        return self.translate(other-self.point(.5,.5,0,"ppp"))
    else:
        return self.against(other,-Z,-Z,X,X,offset,adjustEdges,adjustAxis)

def _move_on_left_of(self,other, offset=(0,0,0),adjustEdges=None,adjustAxis=None):
    if is_point(other):
        return self.translate(other-self.point(1,.5,.5,"ppp"))
    else:
        return self.against(other,X,X,Y,Y,offset,adjustEdges,adjustAxis)
def _move_on_right_of(self,other, offset=(0,0,0),adjustEdges=None,adjustAxis=None):
    if is_point(other):
        return self.translate(other-self.point(0,.5,0.5,"ppp"))
    else:
        return self.against(other,-X,-X,Y,Y,offset,adjustEdges,adjustAxis)
def _move_in_front_of(self,other, offset=(0,0,0),adjustEdges=None,adjustAxis=None):
    if is_point(other):
        return self.translate(other-self.point(.5,1,.5,"ppp"))
    else:
        return self.against(other,Y,Y,X,X,offset,adjustEdges,adjustAxis)
def _move_behind(self,other, offset=(0,0,0),adjustEdges=None,adjustAxis=None):
    if is_point(other):
        return self.translate(other-self.point(.5,0,0.5,"ppp"))
    else:
        return self.against(other,-Y,-Y,X,X,offset,adjustEdges,adjustAxis)




def _show_box(self):
    """
    constructs a Polyhedral corresponding to the Framebox, glued_on self. The colors of the polyhedral corresponds to the axis. 
    """
    b=self.box()   
    liste=[b.plane(-X,-.00001,"p"),b.plane(X,1.00001,"p"),b.plane(-Y,-.00001,"p"),b.plane(Y,1.00001,"p"),b.plane(-Z,-.00001,"p"),b.plane(Z,1.00001,"p")]
    # the above planes are slightly moved from their real location to avoid a dirty display when self has a face on one of the planes.
    colors=["Red","Scarlet","Green","ForestGreen","Cyan","Blue"]
    for i in range(6):
        liste[i].colored(colors[i])
    cube=liste.pop().intersected_by(liste,keepTexture=False,takeCopy=False).glued_on(self)
    for i in range(3):
        center=b.point(0.5,0.5,0.5)
        boxOrigin=b.point(0,0,0)
        en=[0,0,0]
        en[i]=1
        end=b.point(*en)
        myList=[0,1,2]
        myList.remove(i)
        en=[0,0,0];en[myList.pop()]=1
        distance=(boxOrigin-b.point(*en)).norm
        en=[0,0,0];en[myList.pop()]=1
        distance=min(distance,(boxOrigin-b.point(*en)).norm)
        cyl=ICylinder.from_point_vector_radius_amputation(center,end-boxOrigin,distance*.25).colored(colors[2*i+1])
        cyl.glued_on(cube)
    return self

ObjectInWorld.hooked_on=_hooked_on
ObjectInWorld.parallel_to=_parallel_to
ObjectInWorld.move_at=_move_at #     # HIGHLY deprecated. DO NOT USE PLEASE. ADD A hook and use hooked_on please
ObjectInWorld.below=_move_below
ObjectInWorld.above=_move_above
ObjectInWorld.in_front_of=_move_in_front_of
ObjectInWorld.behind=_move_behind
ObjectInWorld.on_left_of=_move_on_left_of
ObjectInWorld.on_right_of=_move_on_right_of
ObjectInWorld.show_box=_show_box


