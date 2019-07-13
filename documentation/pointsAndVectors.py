
pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core"
import os
thisFileAbsName=os.path.abspath(__file__)
pycaoDir=os.path.dirname(thisFileAbsName)+"/../core"

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


yellowPoint=point(1,2,3)
blueVector=vector(1,0,0)
greenVector=vector(2,0,0)
orangePoint=yellowPoint+blueVector
redPoint=greenVector+orangePoint

"""
print("Blue+Green")
print(blueVector+greenVector)
print("Red-Yellow")
print(redPoint-yellowPoint)
print("Red")
print(redPoint)
print("Yellow")
print(yellowPoint)
"""

def gVector(start,end,cylinderRadius,arrowPercentage,arrowRadius,color):
    #print(start)
    start=start.clone()
    #print(start)
    end=end.clone()
    endCylinder=(1-arrowPercentage)*start+arrowPercentage*end
    basket=ObjectInWorld()
    cyl=Cylinder(start,endCylinder,cylinderRadius)
    cyl.colored(color)
    cone=Cone(endCylinder,end,arrowRadius,0)
    cone.colored(color)
    #print(cone)
    cone.glued_on(basket)
    cyl.glued_on(basket)
    return basket

yp=Sphere(yellowPoint,0.1).colored("Yellow")
op=Sphere(orangePoint,0.1)
op.colored("Orange")
rp=Sphere(redPoint,0.1)
rp.colored("Red")
bv=gVector(yellowPoint,orangePoint-.1*X,0.05,0.8,0.15,"Blue")
gv=gVector(orangePoint,redPoint-.1*X,0.05,0.8,0.15,"Green")


light=Light() # a light
light.location=(origin+6.8*Z-2*X+Y)

camera=Camera()
camera.zoom(.3)
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.location=origin-0*X+10*Y+4*Z
camera.lights=[light]
camera.actors=[yp,op,rp,bv,gv] # what is seen by the camera
camera.lookAt=op.center+1.2*Y
camera.zoom(4)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 


camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
