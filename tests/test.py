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



pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit/distributed"

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
from architecturelibrary import *

"""
                SCENE DESCRIPTION
"""

# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.color='DarkGreen' # The possible colors are the colors described in colors.inc in povray or a rgb color. 

#wall=Room(Polyline([origin,X,X+Y,Y,-2*X,-Y])).colored("Yellow")
table=Chair().colored("White").translate(.5*Z)

light=Light() # a light
light.location=(origin+6.8*Z-2*X+Y)

camera=Camera()
camera.projection="orthographic"
camera.projection="perspective"
camera.filmAllActors=False
print(camera.file)
camera.location=origin-0*X-2*Y+2*Z
camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
#camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
camera.actors=[table,ground,table] # what is seen by the camera
camera.lookAt=origin
camera.zoom(0.4)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 


camera.angle=0.84
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
