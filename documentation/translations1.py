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
light=Light().hooked_on(camera.hook()+3*X-Z) # a light located close to the camera
light.glued_on(camera) # the light will follow the camera, so that you will get light on your objects


#######################################

"""
                SCENE DESCRIPTION
"""





# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('Gray') # The possible colors are the colors described in colors.inc in povray or a rgb color as in the exemple below. 

#bbloc1
redCube=Cube(2,4,6).colored("Red")
redCube.add_hook("top",point(1,2,6)) # usually done at creation time when the coordinates are easy to understand
redCube.add_hook("center",point(1,2,3)) # an other hook. The active hook of redCube is "center" as it is created. The previous hook "top" is still known but not selected. 
redCube.hooked_on(point(2.2223,3.5672,4.345)) # moves the hook "center" to a random destination point and the cube follows
greenCube=Cube(1,2,3).colored("Green") 
greenCube.add_hook("bottom",point(.5,1,0))
redCube.select_hook("top") # we change the active hook
greenCube.hooked_on(redCube) # sends the active hook "bottom" of greenCube to the active hook "top" of redCube
#ebloc1








#################################################
#  Now, what you see
#################################################


camera.hooked_on(origin-4*Y+10*Z)  # the positive y are in front of us because the camera is located in negative Y and we look at  a point close to the origin
camera.lookAt=greenCube.hook() # look at the center of cyl
camera.actors=[ground,redCube,greenCube] # what is seen by the camera
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.5)
camera.imageHeight=600 # in pixels
camera.imageWidth=400 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
#camera.show
