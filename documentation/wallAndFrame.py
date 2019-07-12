pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao"

import os 
import sys
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac
import math

from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
from povrayshoot import *
from cameras import *
from lights import *

ground=plane(Z,origin)
ground.color='Gray'

wall=Cube(0.2,5,2.5)
wall.color="Brown"

picture=Cube(0.05,1,0.4)
picture.color='MediumSeaGreen'

nail=Sphere(picture.point(1,0.5,1,"ppp")+0.02*X,0.07)
nail.color="Orchid"
nail.glued_on(picture)

t=Sphere(origin,0.12)

p=picture.point(0.5,0.5,0.5,"ppp")
p=nail.center
q=wall.point(0.5,4,0.5,"pan")
picture.against(wall,-X,X,Y,-Y,offset=-0.05*X,adjustAxis=[p,q])

table=Cube(1.5,0.8,0.07)
table.color='Black'
pied1=Cube(0.05,0.05,0.7)
pied2=pied1.clone()
pied3=pied1.clone()
pied4=pied1.clone()
pied1.against(table,Z,Z,X,X,adjustEdges=Y+X)
pied2.against(table,Z,Z,X,X,adjustEdges=Y-X)
pied3.against(table,Z,Z,X,X,adjustEdges=-Y-X)
pied4.against(table,Z,Z,X,X,adjustEdges=-Y+X)
for pied in [pied1,pied2,pied3,pied4]:
    pied.glued_on(table)
M=Map.translation(-pied1.point(0,0,0,"ppp")+origin)
print(M)
table.move(M)
table.translate(-1,3,0)
axis=Segment(table.center,table.center+Z)
M=Map.rotation(axis,math.pi/10)
table.move(M)
#screwPositiveRotations=False


light=Light()
light.location=(6.8*Z-2*X+Y)
camera=Camera()
camera.location=origin-5*X+0*Y+2*Z
camera.lights=[light]
camera.actors=[picture,wall,t,table,ground]

#camera.actors=[wall,ground,t]
#camera.actors=[ground,t]
#camera.actors=[picture]
#camera.actors=[ground,picture]
camera.lookAt=wall.center
camera.zoom(2)

#camera.projection="orthographic"
#print(camera.angle)
#camera.directFrame=True

camera.shoot

camera.pov_to_png
