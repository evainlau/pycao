
pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao/core"
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





#bbloc1
ground=plane(Z,origin).colored('SeaGreen')
basket=point(0,0,0)
cub=Cube(.91,.91,.91)
for a in range(3):
    for b in range(3):
        for c in range(3):
            d=cub.clone()
            d.rgbed(c,b,a)
            d.translate(point(a,b,c+0.5)-origin)
            d.glued_on(basket)
# we copy the basket. The elements glued
#on it are also copied recursivly	      
basket2=basket.clone()
basket2.rotate(Segment(origin,origin+X+Y+Z),3.14/3)
basket2.translate(6*X+Z).glued_on(ground)
camera=Camera()
camera.filmAllActors=False
camera.actors=[ground,basket,basket2] # what is seen by the camera wiht the children
#ebloc1


directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/generatedImages/"+os.path.splitext(base)[0]+".pov"
camera.location=origin-10*Y+4*Z
#camera.actors=[basket,basket2] # what is seen by the camera wiht the children
camera.lookAt=.5*(basket2+basket)
camera.lookAt=basket2
camera.zoom(.42512)
l=Light().hooked_on(camera.location-X+Z-Y)
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 


