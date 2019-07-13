
pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/core"
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

# a plane represented graphically as a half space 

c=plane(-Y,origin)
#c=plane(origin,origin-Z,origin+X).reverse()


d=plane(-X,origin)
e=plane(Z,origin)

#c.color="Yellow"
d.color="Red"
e.color="Green"


f=Polyhedral([c,d,e])
#f.color="Gray"

light=Light() # a light
light.location=(origin+2.8*Z-2*X-Y)



camera=Camera()
camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
camera.location=origin-15*X-4*Y+5*Z
camera.lights=[light]
camera.actors=[f] # what is seen by the camera
camera.lookAt=origin+0*Z

camera.zoom(1)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 


camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 

