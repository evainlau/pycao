
pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao/core"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/core/"

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


brownCube=Cube(3,5,7) # The two opposite corners of the cube are origin and point(1,2,3)
brownCube.color="Brown"
brownCube.move_at(origin) # the cube is moved above the plane

yellowCube=Cube(1,1,1)
yellowCube.color="Yellow   "
yellowCube.move_at(origin-5*X-3*Z-6*Y) # the cube is moved above the plane


xaxis=FrameAxis(brownCube.center,brownCube.center+7*X,0.9,0.6,1.6)
xaxis.color='Red'
yaxis=FrameAxis(brownCube.center,brownCube.center+7*Y,0.9,0.6,1.6)
yaxis.color='Green'
zaxis=FrameAxis(brownCube.center,brownCube.center+7*Z,0.9,0.6,1.6)
zaxis.color='NavyBlue'


xaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*X,0.9,0.3,1)
xaxisg.color='Red'
yaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Y,0.9,0.3,1)
yaxisg.color='Green'
zaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Z,0.9,0.3,1)
zaxisg.color='NavyBlue'
xaxisg.glued_on(yellowCube)
yaxisg.glued_on(yellowCube)
zaxisg.glued_on(yellowCube)
xaxis.glued_on(brownCube)
yaxis.glued_on(brownCube)
zaxis.glued_on(brownCube)




yellowCube.against(brownCube,-Z,X,X,Y,adjustEdges=X-Y, offset=-Z)
yellowCube.glued_on(brownCube)
diagonal=Segment(brownCube.point(0,0,0,"ppp"),brownCube.point(1,1,1,"ppp"))
M=Map.rotational_difference(diagonal.vector,Z)
brownCube.move(M)

#yellowCube.against(brownCube,-Z,X,X,Y)


light=Light() # a light
light.location=(origin+6.8*Z-2*X+Y)

camera=Camera()
camera.location=origin-15*X+5*Y+10*Z
camera.lights=[light]
camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
camera.actors=[brownCube,yellowCube,xaxis,yaxis,zaxis,xaxisg,yaxisg,zaxisg] # what is seen by the camera
#camera.actors=[xaxis] # what is seen by the camera
camera.lookAt=xaxis.arrow.center
camera.zoom(0.8)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 


camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
