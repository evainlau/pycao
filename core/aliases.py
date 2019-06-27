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

import os 
import sys
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac

from uservariables import *
from generic import *
from mathutils import *



 
################
"""
    global math objects
"""
################

# def vector(*args):
#     """
#     The input arguments are 
#     a triplet for the coordinates of the vector
#     or an np.array
#     """
#     if len(args)==3:
#         return MassPoint(args[0],args[1],args[2],0)
#     elif len(args)==1:
#         return MassPoint(args[0][0],args[0][1],args[0][2],0)



# X=vector(1,0,0)
# Y=vector(0,1,0)
# Z=vector(0,0,1)
# point=Point
# T=point(0,0,0)
# origin=T
# Origin=T

# Base.canonical=Base(X,Y,Z,T)
# Map.identity=Map.affine(X,Y,Z,T)


Vector=vector
plane=AffinePlaneWithEquation
Plane=plane
line=Segment
Line=line


# def is_vector(self):
#     return isinstance(self,MassPoint) and (self[3]==0)

# def is_point(self):
#     return isinstance(self,MassPoint) and (self[3]==1)
