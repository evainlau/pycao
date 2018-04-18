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



pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit/distributed"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/distributed"
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
from architecturelibrary import *

"""
                SCENE DESCRIPTION
"""

# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.color='DarkGreen' # The possible colors are the colors described in colors.inc in povray or a rgb color. 
wallColor="pigment{ color rgb <0.75,0.5,0.3>} "

#wall=Room(Polyline([origin,X,X+Y,Y,-2*X,-Y])).colored("Yellow")
room=Room(Polyline([origin,7.012*Y,11.526*X,-5.64*Y,-3.614*X,-1.386*Y,-7.912*X]),insideThickness=.31).colored("White")
room.floor.colored("OldGold")
#wall=RoundWindow(radius=1,depth=.1,border=.1,texture="Yellow_Pine")
room.add_window(wallNumber=0,wlength=1.8,wheight=2.15,wdepth=.1,deltaLength=4.106,deltaHeigth=0)
backDoor=room.add_door(wallNumber=1,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=5.756,deltaHeigth=0)#
room.add_window(wallNumber=2,wlength=1,wheight=1.06,wdepth=.1,deltaLength=1.37,deltaHeigth=1.10)
room.add_window(wallNumber=2,wlength=.7,wheight=1.05,wdepth=.1,deltaLength=3.57,deltaHeigth=1.10)
room.add_window(wallNumber=3,wlength=.7,wheight=.7,wdepth=.1,deltaLength=2.57,deltaHeigth=1.60)
outsideDoor=room.add_door(wallNumber=4,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=.13,deltaHeigth=0,reverseHandle=True).colored("BrightGold").add_porthole()#
room.add_window(wallNumber=5,wlength=2.2,wheight=2.15,wdepth=.1,deltaLength=1.056,deltaHeigth=0)
room.add_window(wallNumber=5,wlength=1.8,wheight=1.05,wdepth=.1,deltaLength=4.056,deltaHeigth=1.1)
room.add_perpendicular_wall(0,distance=2.74,wallLength=2.70,thickness=.08,measurementType="a",height=None).colored("Silver")
room.add_perpendicular_wall(1,distance=3.73+.85,wallLength=1.67+1.47,thickness=.08,measurementType="a",height=None).colored("Silver")
room.add_perpendicular_wall(0,distance=3.31,wallLength=2.9,thickness=.08,measurementType="a",offset=3.73+.83,height=None).colored("Silver")#wall8
room.add_perpendicular_wall(1,distance=3.4,wallLength=1.67+1.47,thickness=.16,measurementType="n",height=None).colored("Silver")
room.add_perpendicular_wall(2,distance=2.94,wallLength=3.4,thickness=.08,measurementType="a",height=None).colored("Silver")
room.add_perpendicular_wall(2,distance=0.95,wallLength=2.86,thickness=.08,measurementType="n",offset=.75,height=None).colored("Silver")
room.add_perpendicular_wall(3,distance=.08,wallLength=.9,thickness=.16,measurementType="n",height=None).colored("Silver")
room.add_perpendicular_wall(3,distance=1.88,wallLength=.9,thickness=.08,measurementType="a",height=None).colored("Silver")
room.add_perpendicular_wall(3,distance=1.6,wallLength=1.1,thickness=.08,measurementType="a",offset=.95,height=None).colored("Silver")
room.add_perpendicular_wall(3,distance=2.3,wallLength=1.1,thickness=.08,measurementType="a",offset=.95,height=None).colored("Silver")
for w in room.walls:
    w.texture=wallColor
door1=room.add_door(wallNumber=8,wlength=.83,wheight=2.15,wdepth=.1,deltaLength=1.45).colored("BrightGold")#
door1.name="porte1"





entrance=point(7,1,2)
floorCenter=origin+3.5*Y+5.6*X
light1=Light(origin+4.8*Z-6*X-4*Y) # a light
light2=Light(floorCenter+2*Z,color="White") # a light
light3=Light(origin+2.3*Z+8*X+2.7*Y,color="White") # a light
light4=Light(origin+2.3*Z+2*X+4.5*Y,color="DarkOliveGreen") # a light
light5=Light(origin+2.3*Z+2*X+1*Y,color="DarkOliveGreen") # a light

table=Table(1.2,.8,.7,.03).colored("White").above(origin+4.8*X+1.5*Y).glued_on(room)
#table=Table(1.5,.8,1,.03).colored("White").glued_on(room)
chair1=Chair().colored("White").above(origin+4.5*X+1.87*Y+.4*Z).glued_on(room)
chair2=chair1.copy()
chair2.colored("White").above(origin+5*X+1.8*Y+.4*Z).glued_on(room)
chair2=Chair().colored("White").above(origin+4.5*X+1*Y+.4*Z).glued_on(room).self_rotate(3)
chair2=Chair().colored("White").above(origin+5*X+1*Y+.4*Z).glued_on(room).self_rotate(3.5)
stovePosistionOnFloor=origin+7.50*X+2.3*Y
stove=Stove().glued_on(room).self_rotate(-math.pi/2)
stove.translate(stovePosistionOnFloor-stove.floorPoint)


camera=Camera()
camera.lights=[light1,light2,light3,light4,light5]
camera.projection="orthographic"
camera.projection="perspective"
camera.filmAllActors=False
print(camera.file)
#camera.location=floorCenter+2*Z-2*X
#camera.location=origin+4*X+2*Z+.5*Y
#camera.location=entrance-X
camera.location=origin+X+Y+2*Z
camera.povraylights="" #"light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
#camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
camera.actors=[room,ground,table] # what is seen by the camera
#camera.actors=[outsideDoor] # what is seen by the camera
camera.lookAt=point(1,3,1)#door1.center+2*X
camera.lookAt=outsideDoor.center#door1.center+2*X
camera.zoom(0.3)
camera.imageHeight=800 # in pixels
camera.imageWidth=900 
camera.angle=1.07
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
