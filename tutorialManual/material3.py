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
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core/"
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

#######################################

"""
                SCENE DESCRIPTION
"""

#bbloc1
p=plane(Z,origin)
pig1=Pigment.from_photo("woodFloor1.png",dimx=2,dimy=2,symmetric=True) # a pigment constructed by Pycao
pig2=Pigment.from_photo("oak.png",dimx=2.,dimy=2.,symmetric=True) # a pigment constructed by Pycao
pig3=Pigment("Blue")
pig4=Pigment("Red")
pig=Pigment.from_square(pig1,pig2,pig3,pig4)
p.textured(pig)
#ebloc1
#p.textured(text) # we apply on our object



#################################################
#  Now, what you see
#################################################


directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/generatedImages/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"/../images/" # where you put your images,photos for the textures
print (camera.povraypath)
camera.zoom(0.655)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=11 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin#+3*X+.75*Z # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+1.6*X-4*Y+3.6*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(origin+8*X+10*Z) # a light located close to the camera
light=Light().hooked_on(origin+8*X+.2*Y+10*Z) # a light located close to the camera
light=Light().hooked_on(origin+8*X-.3*Y+10*Z) # a light located close to the camera
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
#camera.pov_to_png_without_viewer # if you want only the photo but not the graphical interface
