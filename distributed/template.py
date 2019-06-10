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



pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit"

"""
                MODULES IMPORT
"""


import os 
import sys
from os.path import expanduser
sys.path.append(pycaoDir)
import math



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
                SCENE DESCRIPTION
"""

# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('Gray') # The possible colors are the colors described in colors.inc in povray or a rgb color. 

wall=Cube(1,2,3) # The two opposite corners of the cube are origin and point(1,2,3)
wall.colored('Brown')
wall.move_at(origin+1.5*Z) # the cube is moved above the plane

cyl=Cylinder(start=origin+2*Y,end=origin+2*Y+Z,radius=0.5) # a vertical Cylinder
cyl.colored('SpicyPink')

axis=Segment(point(0,4,0),point(0,4,1))
cyl2=ICylinder(axis,0.5) #an infinite cylinder of radius 0.5
cyl2.new_texture("pigment { brick Black Green brick_size 2 mortar 0.2 }")


s=Sphere(point(0,6,0),1)
s.rgbed(1.5,0.5,0.5,1)# three rgb colors + facultative transparency


light=Light() # a light
light.location=(origin+6.8*Z-2*X+Y)

camera=Camera()
camera.location=origin-5*X+0*Y+2*Z
camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
camera.lookAt=cyl.center
camera.zoom(0.1)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 


camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
