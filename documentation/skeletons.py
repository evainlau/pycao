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

#######################################

"""
                SCENE DESCRIPTION
"""

if 1>0:
    import armature
    from armature import *
    g=plane(Z,origin-Z).colored("Grey")
    body1=Body(topHeadHeight=1.805,
                 armup=2.34, # the height of the end of the nails, when the arm is up
                 armdown=.69,# the height of the end of the nails, when the arm is down
                 topShoulder=1.54, #the height above the shoulder
                 bottomMentonHeight=1.57, 
                 headCirconference=.6,
                 neckCirconference=.4,
                 leftRightLegAxes=.12,# the distance between the legs axes, when they are parallels. 
                 leftRightArmAxes=.44, # idem for the arms
                 wristFinger=.22,# full distance from the wris to the end of  the nails, when the wrist is bent at 90 degrees 
                 elbowWrist=.325,# full distance from the wris to the elbow, when the wrist is bent at 90 degrees 
                 elbowFinger=.51,# lower arm, including elbow,
                 belowElbow=1.105,#, the height below the elbow, when the elbow is bent at 90 degrees horizontally
                 ankleHeight=.1,# the height of the proeminent point of the ankle
                 ankleWidth=.065,# measured at the proeminent points of the ankle
                 lowerLeg=.58, #ground to above the knee, when sit on a chair
                 upperLeg=.67, #distance from the back to to above the knee, when sit on a chair
                 leg=1.14,# sit on the ground, the back on a wall, distance from the wall to the foot arches
                 upperBody=.63, #height of the top of a shoulder, when sit on the ground
                 footSize=[.10,.28,None],
                 shoeSole=.02, # thickness of the sole
                 yDistanceAnkleToe=.2,# horizontal distance from the center of the ankle to the end of nails
                 handWidth=.1, 
                 handThickness=.025,
                 tibiaLowerCirconference=.24,
                 tibiaUpperCirconference=.37,
                 femurLowerCirconference=.4,
                 femurUpperCirconference=.62,
                 humerusLowerCirconference=.28,
                 humerusUpperCirconference=.36,
                 cubitusLowerCirconference=.175,
                 cubitusUpperCirconference=.30,
                 trunkLowerCirconference=.9,
                 trunkLowerWidth=.35,
                 trunkUpperCirconference=1.03)   


    
    body2=Body().translate(X)
    body2.bend.leftShoulder(1.6,X) # arguments=(angleInRadians,axisVectorForTHeRotation) 
    body3=Body().translate(2*X)
    body3.bend.leftShoulder(1.6,X,toggleJoint=True)
    
    # We take a  photo
    camera=Camera()
    light=Light().hooked_on(camera.hook()+1*X+1*Z) # a light located close to the camera
    camera.file="skeleton.pov"
    directory=os.path.dirname(os.path.realpath(__file__))
    base=os.path.basename(__file__)
    camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
    camera.filmAllActors=False
    camera.location=origin-7*Y+3.2*Z
    camera.zoom(1.6)
    camera.lookAt=origin+X+Z
    camera.actors=[g,body1,body2,body3]
    camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
    camera.pov_to_png # show the photo, ie calls povray. 





#################################################
#  Now, what you see
#################################################
"""
camera.file="pycaoOutput.pov" # A name for the povray file that will be generated. Must end with .pov
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.15)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+0*X-1*Y+1*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(camera.hook()+1*X+1*Z) # a light located close to the camera

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
#camera.show_without_viewer # if you want only the photo but not the graphical interface
"""
