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
light=Light().hooked_on(camera.hook()+1*X+Z) # a light located close to the camera
light.glued_on(camera) # the light will follow the camera, so that you will get light on your objects


#######################################

"""
                SCENE DESCRIPTION
"""





# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('Gray') # The possible colors are the colors described in colors.inc in povray or a rgb color as in the exemple below. 

greenBox=Cube(.5,.3,.2).colored("SeaGreen")
greenBox.add_hook("center",greenBox.center)
yellowDrawer=Cube(.4,.25,.15).colored("Yellow")
yellowDrawer.add_hook("aboveCenter",yellowDrawer.center+.025*Z)
yellowDrawer.add_hook("behindCenter",yellowDrawer.center+.031*Y)
yellowDrawer.hooked_on(greenBox)
greenBox.amputed_by(yellowDrawer,takeCopy=True,throwShapeAway=False)
toCut=Cube(.35,.2,.15)
yellowDrawer.add_hook("back",yellowDrawer.point(.5,1,.5))
greenBox.add_hook("front",greenBox.point(.5,0,.5))                      
toCut.add_hook("center",toCut.center).hooked_on(yellowDrawer)
toCut.colored("Pink")
yellowDrawer.select_hook("aboveCenter")
toCut.hooked_on(yellowDrawer)
yellowDrawer.amputed_by(toCut)


camera.hooked_on(origin-1*Y+0.82*Z)  # the positive y are in front of us because the camera is located in negative Y and we look at  a point close to the origin
camera.lookAt=yellowDrawer.center # look at the center of cyl
camera.actors=[ground,greenBox,yellowDrawer] # what is seen by the camera


if 1>0:
    # def of the drawer switched"
    yellowDrawer.add_axis("axis",line(origin,origin+Y)) #The vector of the axis is v=Y
    camera.file="docPictures/drawerClosed.pov"
    camera.shoot
    camera.pov_to_png
    #camera.show
    yellowDrawer.self_translate(-.1) # moves by -.1*v=-.1*Y
    camera.file="docPictures/drawerOpen.pov"
    camera.shoot
    camera.pov_to_png
    #camera.show
    yellowDrawer.select_hook("back") # A point in the back of the drawer
    greenBox.select_hook("front") # A point in the front of the greenBox
    yellowDrawer.self_gtranslate(greenBox)
    camera.file="docPictures/drawerFullOpen.pov"
    camera.shoot
    camera.pov_to_png
    #camera.show
#################################################
#  Now, what you see
#################################################

#camera.actors=[yellowDrawer,toCut] # what is seen by the camera
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.8)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene

#camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
#camera.pov_to_png # show the photo, ie calls povray. 
