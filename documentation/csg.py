
pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao"
pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core"

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
ground.color='Gray' # The possible colors are the colors described in colors.inc in povray or a rgb color. 

wall=Cube(2,2,2) # The two opposite corners of the cube are origin and point(1,2,3)
wall.color="Brown"
wall.name="wall"
wall.move_at(origin+1*Z) # the cube is moved above the plane

#cyl=Cylinder(start=origin,end=origin+5*Z,radius=0.5) # a vertical Cylinder
#cyl.color='SpicyPink'


axis=Segment(point(0,0,0),point(0,0,1))
#cyl2=ICylinder(axis,0.25) #an infinite cylinder of radius 0.5
#cyl2.color='Yellow'

#cyl.amputed_by(cyl2,throwShapeAway=True)
#wall.amputed_by(cyl)

axis.translate(3,0,0)
cyl3=ICylinder(axis,0.2)
cyl3.visibility=0
#axis.translate(-6,0,0)
cyl4=ICylinder(axis,3.5)
cyl4.visibility=0
#cyl4.glued_on(cyl3)
#print(wall.csgOperations)
#f=Cube(2,2,2)
f=wall.clone()
f.translate(-0.5,0.5,0.5)
#f.visibility=0
#f.booleanVisibility=0
f.glued_on(cyl3)
#print(wall.csgOperations)

#f.translate(0,0,0)
#f.glued_on(cyl4)
for tool in cyl3.descendants_and_myself():
    #print(tool)
    wall.amputed_by(tool)

#print(wall.csgOperations)

light=Light() # a light
light.location=(origin+6.8*Z-2*X+Y)

camera=Camera()
camera.location=origin-5*X-2*Y+10*Z
camera.lights=[light]
camera.actors=[wall,f] # what is seen by the camera
#camera.actors=listOfAllObjects # what is seen by the camera
camera.lookAt=wall.center
camera.zoom(4.8)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 


camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
