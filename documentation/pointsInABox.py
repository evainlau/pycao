
pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao"

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

w=Cube(3,3,3)
diagonal=Segment(w.point(0,0,0,"ppp"),w.point(1,1,1,"ppp"))
M=Map.rotation(diagonal,-math.pi/4)
w.move(M)


w.color='Brown'
s=Sphere(w.point(0,0.3,0.5,"aap"),.1)
s.color="Blue"
t=Sphere(w.point(0,0.3,0.5,"anp"),.1)
t.color="Green"
u=Sphere(w.point(0,0.3,0.5,"app"),.1)
u.color="Grey"

seg=w.boxline(0.5,0.5,None,"ppp")
cyl=ICylinder(seg,0.2)
cyl.color='SpicyPink'
seg2=w.boxline(0.5,None,0.5,"ppp")
cyl2=ICylinder(seg2,0.2)
cyl2.color='Yellow'

p=w.boxplane(X,0.6,"p")
p.color="Orange"


light=Light() # a light
light.location=(origin+6.8*Z-2*X+Y)

camera=Camera()
camera.location=origin+10*(-10*X-2*Y+4*Z)
camera.lights=[light]
camera.actors=[w,s,t,u,cyl,cyl2,p] # what is seen by the camera
camera.lookAt=w.center
camera.zoom(20)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 


camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
