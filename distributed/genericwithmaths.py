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

def _rotate_object(self,axis,angle):
    self.move(Map.rotation(axis,angle))
    return self

def _scale_object(self,fx=1,fy=1,fz=1,xVector=X,yVector=Y, zVector=Z,fixedPoint=T):
    self.move(Map.scale(fx=fx,fy=fy,fz=fz,xVector=xVector,
                        yVector=yVector, zVector=zVector,fixedPoint=fixedPoint))
    return self


@staticmethod
def _new_object(cls,*args,**kwargs):
    #dico={handle.name:handle for handle in handles}
    self=super(ObjectInWorld,cls).__new__(cls)
    ObjectInWorld.__init__(self,args,kwargs)
    return self

def _init_object(self,*args,**kwargs):
    keys = sorted(kwargs.keys())
    if "name" in keys:
        self.name=kwargs["name"]
    self.materials=[]
    if "material" in keys:
        self.materials.append(kwargs["material"])
#    else:
#        self.materials.append(DEFAULT_COLOR)
    self.mapFromParts=Map.identity
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
    self.color=None
    self.csgOperations=[]
    #print (allObjects)
    #print(self)
    #print ([self is object for object in listOfAllObjects])
    if not any([self is object for object in listOfAllObjects]):
        listOfAllObjects.append(self)

# def is_vector_object(self):
#     return isinstance(self,MassPoint) and (self[3]==0)

# def is_point_object(self):
#     return isinstance(self,MassPoint) and (self[3]==1)





ObjectInWorld.translate=_translate_object
ObjectInWorld.rotate=_rotate_object
ObjectInWorld.scale=_scale_object
ObjectInWorld.__init__=_init_object
ObjectInWorld.__new__=_new_object
#object.is_vector=is_vector_object
#object.is_point=is_point_object

#print (vector)

def _move_at(self,*location):
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
    #print("Translation de vecteur")
    #print(vector)
    #print(self)
    #print(self.translate(vector))
    return self.translate(vector)


BoundedByBox.move_at=_move_at
