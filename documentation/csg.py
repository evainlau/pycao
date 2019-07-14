
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



#bbloc1
wall=Cube(2,2,2).colored("Brown").translate(origin-X-Y+.5*Z) # the cube is moved above the plane

cyl=Cylinder(start=origin,end=origin+5*Z,radius=0.5).colored('SpicyPink')

axis=Segment(point(0,0,0),point(0,0,1))
cyl2=ICylinder(axis,0.25).colored('Yellow') #an infinite cylinder 


# Using amputations : corresponds to the yellow and pink marks since the elements amputed don't keep their textures
cyl.amputed_by(cyl2,keepTexture=False)
wall.amputed_by(cyl,keepTexture=False)

# Using intersection : no change of colors since keepTexture is true by default.
axis.translate(3,0,0)
cyl3=ICylinder(axis,3.2).colored("Green")
axis.translate(-6,0,0)
cyl4=ICylinder(axis,3.5).rgbed(1,1,1)
wall.intersected_by([cyl3,cyl4])
wall.rotate(Segment(origin,Z),.5)
#ebloc1

camera=Camera()
camera.file="csg.pov"
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.filmAllActors=True
#camera.actors=[wall]
#camera.actors=[cyl]
camera.location=origin-4*X+5.2*Z
camera.zoom(0.8)
camera.lookAt=(origin+Z)
l=Light().hooked_on(camera.location+X)
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
