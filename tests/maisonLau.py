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

import os 
if os.environ['ordi']=="ordiFac":
    pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/distributed"
else:
    pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit/distributed"
#
"""
                MODULES IMPORT
"""



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
from material import *
import povrayshoot 
from cameras import *
from lights import *
from material import *
from architecturelibrary import *

"""
                SCENE DESCRIPTION
"""

# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('DarkGreen') # The possible colors are the colors described in colors.inc in povray or a rgb color. 


#wall=Room(Polyline([origin,X,X+Y,Y,-2*X,-Y])).colored("Yellow")
room=Room(Polyline([origin,7.012*Y,11.526*X,-5.64*Y,-3.614*X,-1.386*Y,-7.912*X]),insideThickness=.31).colored("LightWood")
room.floor.makeup(Texture.from_colorkw("DarkBrown"))#("OldGold")
unleash([room.floor])
room.floor.name="myFloor"
normale="normal{ quilted 2 control0 0 control1 0 scale .3}"
room.floor.texture.enhance(normale)
print("apres la normale",room.floor.texture.smallString)
room.ceiling.makeup(Texture.from_colorkw("White"))#("OldGold")
print("apres le ceiling",room.floor.texture.smallString)
#tex=room.floor.texture.copy().enhance("normal {brick brick_size .4 mortar .003}")
#room.floor.makeup(tex)
#wall=RoundWindow(radius=1,depth=.1,border=.1,texture="Yellow_Pine")
myWin=room.add_window(wallNumber=0,wlength=1.8,wheight=2.15,wdepth=.1,deltaLength=4.106,deltaHeigth=0).colored("White")
backDoor=room.add_door(wallNumber=1,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=5.756,deltaHeigth=0)#
room.add_window(wallNumber=2,wlength=1,wheight=1.06,wdepth=.1,deltaLength=1.37,deltaHeigth=1.10).colored("White")
room.add_window(wallNumber=2,wlength=.7,wheight=1.05,wdepth=.1,deltaLength=3.57,deltaHeigth=1.10).colored("White")
room.add_window(wallNumber=3,wlength=.7,wheight=.7,wdepth=.1,deltaLength=2.57,deltaHeigth=1.60).colored("White")
outsideDoor=room.add_door(wallNumber=4,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=.13,deltaHeigth=0,reverseHandle=True).colored("BrightGold")
outsideDoor.add_porthole()
outsideDoor.window.frame.rgbed([.8,.8,.6])
outsideDoor.name="outsideDoor"
tex=outsideDoor.texture.enhance("normal {brick brick_size 1.5 mortar .05} ").move(Map.linear(X,Y,2*Z))
outsideDoor.makeup(tex)
room.add_window(wallNumber=5,wlength=2.2,wheight=2.15,wdepth=.1,deltaLength=1.056,deltaHeigth=0).frame.colored("White")
room.add_window(wallNumber=5,wlength=1.8,wheight=1.05,wdepth=.1,deltaLength=4.056,deltaHeigth=1.1).frame.colored("White")

room.add_perpendicular_wall(0,distance=2.74,wallLength=2.70,thickness=.08,measurementType="a",height=None).colored("LightWood")
room.add_perpendicular_wall(1,distance=3.73+.85,wallLength=1.67+1.47,thickness=.08,measurementType="a",height=None).colored("LightWood")
room.add_perpendicular_wall(0,distance=3.31,wallLength=2.9,thickness=.08,measurementType="a",offset=3.73+.83,height=None).colored("LightWood")#wall8
room.add_perpendicular_wall(1,distance=3.4,wallLength=1.67+1.47,thickness=.16,measurementType="n",height=None).colored("LightWood")
room.add_perpendicular_wall(2,distance=2.94,wallLength=3.4,thickness=.08,measurementType="a",height=None).colored("LightWood")
room.add_perpendicular_wall(2,distance=0.95,wallLength=2.86,thickness=.08,measurementType="n",offset=.75,height=None).colored("LightWood")
room.add_perpendicular_wall(3,distance=.08,wallLength=.9,thickness=.16,measurementType="n",height=None).colored("LightWood")
room.add_perpendicular_wall(3,distance=1.88,wallLength=.9,thickness=.08,measurementType="a",height=None).colored("LightWood")
room.add_perpendicular_wall(3,distance=1.6,wallLength=1.1,thickness=.08,measurementType="a",offset=.95,height=None).colored("LightWood")
room.add_perpendicular_wall(3,distance=2.3,wallLength=1.1,thickness=.08,measurementType="a",offset=.95,height=None).colored("LightWood")
for w in room.walls:
    w.rgb=[0.75,0.5,0.3]
door1=room.add_door(wallNumber=8,wlength=.83,wheight=2.15,wdepth=.1,deltaLength=1.45).colored("BrightGold")#
door1.name="porte1"
door1.makeup(tex)



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
table.name="table"
chair1=Chair().colored("Khaki").above(origin+4.5*X+1.87*Y+.4*Z).glued_on(table)
chair2=chair1.copy()
chair2.colored("Khaki").above(origin+5*X+1.8*Y+.4*Z).glued_on(table)
chair2=Chair().colored("Khaki").above(origin+4.5*X+1*Y+.4*Z).glued_on(table).self_rotate(3)
chair2=Chair().colored("Khaki").above(origin+5*X+1*Y+.4*Z).glued_on(table).self_rotate(3.5)
table.translate(.82*X)
stovePosistionOnFloor=origin+7.50*X+2.3*Y
stove=Stove().glued_on(room).self_rotate(-math.pi/2)
stove.name="stove"
stove.translate(stovePosistionOnFloor-stove.floorPoint)
stove.spacer.texture.enhance("finish {ambient 0.05}")

print("avant le light level",room.floor.texture.smallString)
print("avant le light level",room.floor.texture.smallString)
room.light_level(1)
camera.projection="orthographic"
camera.projection="perspective"
#camera.location=origin+1.6*X+1.5*Y+1.62*Z
camera.location=entrance-3.9*X+1*Y-.3*Z
camera.actors=[room,ground] # what is seen by the camera
#camera.actors=[room.floor]
#camera.lookAt=kitchenLamp.light.handle()
camera.lookAt=entrance+1*Y-1.05*Z
camera.angle=1.07
#for light in camera.lights:
#    print(light.povray_string())

print("a la fin",room.floor.texture.smallString)
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
#print (globVars.TextureString)
