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
pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/distributed"
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


#wall=Room(Polyline([origin,X,X+Y,Y,-2*X,-Y])).colored("Yellow")
room=Room(Polyline([origin,7.012*Y,11.526*X,-5.64*Y,-3.614*X,-1.386*Y,-7.912*X]),insideThickness=.31).colored("White")
room.floor.colored("DarkBrown")#("OldGold")
#wall=RoundWindow(radius=1,depth=.1,border=.1,texture="Yellow_Pine")
room.add_window(wallNumber=0,wlength=1.8,wheight=2.15,wdepth=.1,deltaLength=4.106,deltaHeigth=0)
backDoor=room.add_door(wallNumber=1,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=5.756,deltaHeigth=0)#
room.add_window(wallNumber=2,wlength=1,wheight=1.06,wdepth=.1,deltaLength=1.37,deltaHeigth=1.10)
room.add_window(wallNumber=2,wlength=.7,wheight=1.05,wdepth=.1,deltaLength=3.57,deltaHeigth=1.10)
room.add_window(wallNumber=3,wlength=.7,wheight=.7,wdepth=.1,deltaLength=2.57,deltaHeigth=1.60)
outsideDoor=room.add_door(wallNumber=4,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=.13,deltaHeigth=0,reverseHandle=True).colored("BrightGold").add_porthole()#
outsideDoor.shadowsize=10
outsideDoor.name="outsideDoor"
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
    w.rgb=[0.75,0.5,0.3]
door1=room.add_door(wallNumber=8,wlength=.83,wheight=2.15,wdepth=.1,deltaLength=1.45).colored("BrightGold")#
door1.name="porte1"




camera=Camera()

entrance=point(7,1,2)
floorCenter=origin+3.5*Y+5.6*X

sun=Light(origin+100*(5*Z-1*X-4*Y)) # a light
sun.rgbColor=[1,1,1]

livingLamp=Lamp().hooked_on(floorCenter-1.7*Y+2.5*Z).glued_on(ground) # a light
corridorLamp=Lamp(shadowless=False).hooked_on(origin+2.5*Z+8*X+3.15*Y).glued_on(room)
#kitchenLamp=Lamp().hooked_on(origin+2.5*Z+2*X+1.5*Y).glued_on(room)
#unseenLamp=Light().hooked_on(floorCenter-1*Y+1.2*Z+2*X).glued_on(ground) # a light
#unseenLamp.color="rgb <1,1,1>"

#light4=Lamp().hooked_on(origin+2.5*Z+2*X+4.5*Y).glued_on(room)

#light6=Light().hooked_on(floorCenter-5.7*Y+2.5*Z+X).glued_on(room) # a light
#light65=Light().hooked_on(floorCenter-5.7*Y+2*Z+X).glued_on(room) # a light
#light7=Light().hooked_on(floorCenter-1*X-5.7*Y+2.5*Z).glued_on(room) # a light
#light8=Light().hooked_on(origin+3*X+.05*Y+2*Z).glued_on(room) # a light

table=Table(1.2,.8,.7,.03).colored("Khaki").above(origin+4.8*X+1.5*Y).glued_on(room)
table.minimumLight=.0
table.lightAbsorption=.0
table.name="table"
#table=Table(1.5,.8,1,.03).colored("White").glued_on(room)
#table.visibiliy=0
chair1=Chair().colored("Khaki").above(origin+4.5*X+1.87*Y+.4*Z).glued_on(table)
chair2=chair1.copy()
chair2.colored("Khaki").above(origin+5*X+1.8*Y+.4*Z).glued_on(table)
chair2=Chair().colored("Khaki").above(origin+4.5*X+1*Y+.4*Z).glued_on(table).self_rotate(3)
chair2=Chair().colored("Khaki").above(origin+5*X+1*Y+.4*Z).glued_on(table).self_rotate(3.5)
table.translate(.82*X)
stovePosistionOnFloor=origin+7.50*X+2.3*Y
stove=Stove().glued_on(room).self_rotate(-math.pi/2)
stove.translate(stovePosistionOnFloor-stove.floorPoint)
stove.rgb=[.1,.1,.1]
#stove.

camera.projection="orthographic"
camera.projection="perspective"
#camera.location=origin+1.6*X+1.5*Y+1.62*Z
camera.location=entrance-3.9*X+1*Y-.3*Z
camera.actors=[room,ground] # what is seen by the camera
#camera.lookAt=kitchenLamp.light.handle()
camera.lookAt=entrance+1*Y-1.05*Z
camera.angle=1.07
#for light in camera.lights:
#    print(light.povray_string())

print ( povrayshoot.object_string_alone(table,camera))
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
