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



#pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core"
import os
thisFileAbsName=os.path.abspath(__file__)
pycaoDir=os.path.dirname(thisFileAbsName)+"/../core"

import sys
sys.path.append(pycaoDir)


"""
                MODULES IMPORT
"""


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
from material import *



###############################
# By default, lights you will append in the file  are appended to existing cameras. So probably 
# you want to leave the first line defining the camera at the beginning of the file


camera=Camera()
camera.hooked_on(origin+2*X-3*Y+1.6*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
#######################################

"""
                SCENE DESCRIPTION
"""



#################################################
#  Now, what you see
#################################################

if 1>0:
    p=Plane(Z,origin).colored("Grey")
    c=Cube(1,1,1).colored("Bronze")
    l=Light().hooked_on(origin+4*X+5*Z+2.8*Y) # a light. spotlight by Default, emitting everywhere around
    l.colored("Red")
    l.rgbed(0,1,0)
    # Uncomment the following to remove shadow
    #l.shadowlessed()
    # A light which emits cone of lights with defined angles
    l.spotlighted(fullLigthAngle=30,noLightAngle=60,look_at=origin)
    # A light emitting cylinders of light
    l.cylindered(fullLigthRadius=10,noLightRadius=20,look_at=origin)
    # Back to point light
    l.pointlighted()
    # to decrease intensity with distance, ditance parameter is where half of the intensity is achieved. Then decreases fast with a high power
    l.fade(distance=5,power=4)













camera.file="lights.pov" # A name for the povray file that will be generated. Must end with .pov
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.25)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
#camera.pov_to_png_without_viewer # if you want only the photo but not the graphical interface
