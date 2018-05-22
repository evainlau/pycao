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
################################################################

#Functions

################################################################
# s is the proportion lengh(Carrelage+Join)/lengthJoin

myFonc="\n#declare mortar1 = function (x,y,z,s){3*pow(mod(x,1)*s,2)-2*pow(mod(x,1)*s,3) } \n#declare mortar2 = function (x,y,z,s){3*pow(mod(-x,1)*s,2)-2*pow(mod(-x,1)*s,3) }  \n"
globvars.userDefinedFunctions+=myFonc


################################################################

# colors, textures

################################################################


tw=Texture.from_photo("betonRose.png",symmetric=True).move(Map.linear(X+Y,X+Z,X+Y+Z)).move(Map.scale(.5124,.51277,.524))
#texFloor=Texture("Yellow_Pine " ).move(Map.linear(6*X,.3*Z,10*Y))

travertin=Texture.from_photo("travertin.png",symmetric=True)#.scale(3,3,1)
stoveTexture=Texture("pigment {image_map {png \"poele.png\"}}")

#oakTexture=Texture("pigment {image_map {png \"chene.png\"}}")
tableTexture=Texture.from_photo("chene.png").flipXY()


tableBump=Normal("agate .5 scale 4 bump_size .2")

handleTexture=Texture("New_Brass finish{ambient 0.05 specular 2}")
stoveFinish=Finish( "ambient 0.05 brilliance 30")
texDoor=Texture.from_photo("door.png",symmetric=True).declare("texDoor")
lampFinish2=Normal("agate .5 scale .1 bump_size .1")
lampFinish=Finish ("ambient .2 diffuse 2")
texCeil=Texture("pigment {White} finish {ambient .3 }")
chairTexture=Texture.from_photo("chene2.png",symmetric=True)#.move(Map.scale(2,2,2))
chairSeatTexture=Texture.from_photo("cuir.png",symmetric=True).scale(.2,.2,.2)


################################################################
#                Objects
################################################################
# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('DarkGreen') # The possible colors are the colors described in colors.inc in povray or a rgb color. 

floorPolyline=Polyline([origin,7.012*Y,11.526*X,-5.64*Y,-3.614*X,-1.386*Y,-7.912*X+.014*Y])
room=Room(floorPolyline,insideThickness=.31)#.colored("LightWood")
#room.light_level(1.5)
room.add_to_texture(Normal("agate .5 scale 1 bump_size .05"))
rommTexture=room.walls[0]
unleash([room.floor])
room.floor.name="myFloor"
room.ceiling.name="Ceiling"
room.ceiling.new_texture(texCeil)


myTile=RoundBox.from_dimensions(.4,.4,.02,.005)
myTile.new_texture(Texture("T_Stone4"))
myTile.new_texture(travertin)
#tiling=Tiling(myTile,jointWidth=.01,jointHeight=.01,xnumber=23,ynumber=10,polyline=floorPolyline)#.move(.001*Z)
#tiling.hooked_on(origin+.001*Z).glued_on(room)
#tiling.glued_on(room)
#tiling.visibility=0
room.floor.visibility=1
room.floor.new_texture(travertin)
ground.visibility=0



#tex=room.floor.texture.copy().enhance("
#room.floor.new_texture(tex)
#wall=RoundWindow(radius=1,depth=.1,border=.1,texture="Yellow_Pine")
myWin=room.add_window(wallNumber=0,wlength=1.8,wheight=2.15,wdepth=.1,deltaLength=4.106,deltaHeigth=0).colored("White").named("myWin")
backDoor=room.add_door(wallNumber=1,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=5.756,deltaHeigth=0)#
room.add_window(wallNumber=2,wlength=1,wheight=1.06,wdepth=.1,deltaLength=1.37,deltaHeigth=1.10).colored("White")
room.add_window(wallNumber=2,wlength=.7,wheight=1.05,wdepth=.1,deltaLength=3.57,deltaHeigth=1.10).colored("White")
room.add_window(wallNumber=3,wlength=.7,wheight=.7,wdepth=.1,deltaLength=2.57,deltaHeigth=1.60).colored("White")

outsideDoor=room.add_door(wallNumber=4,wlength=.9,wheight=2.15,wdepth=.1,deltaLength=.13,deltaHeigth=0,reverseHandle=True,handleTexture=handleTexture).new_texture(texDoor.copy().flipXZ().flipYZ())
outsideDoor.add_porthole()
outsideDoor.window.frame.rgbed([.8,.8,.6])
outsideDoor.name="outsideDoor"

ls=LightSwitch().parallel_to(-1*room.walls[4].insideVector())
ls.hooked_on(room.walls[4].insideBaseLine().point(.2,"p")+1.1*Z).glued_on(room)

room.add_window(wallNumber=5,wlength=2.2,wheight=2.15,wdepth=.1,deltaLength=1.056,deltaHeigth=0).frame.colored("White")
room.add_window(wallNumber=5,wlength=1.8,wheight=1.05,wdepth=.1,deltaLength=4.056,deltaHeigth=1.1).frame.colored("White")

room.add_perpendicular_wall(0,distance=2.74,wallLength=2.70,thickness=.08,measurementType="a",height=None).new_texture(tw)
room.add_perpendicular_wall(1,distance=3.73+.85,wallLength=1.67+1.47,thickness=.08,measurementType="a",height=None).new_texture(tw)
room.add_perpendicular_wall(0,distance=3.31,wallLength=2.9,thickness=.08,measurementType="a",offset=3.73+.83,height=None).new_texture(tw)#wall8
room.add_perpendicular_wall(1,distance=3.4,wallLength=1.67+1.47,thickness=.16,measurementType="n",height=None).new_texture(tw)
room.add_perpendicular_wall(2,distance=2.94,wallLength=3.4,thickness=.08,measurementType="a",height=None).new_texture(tw)
room.add_perpendicular_wall(2,distance=0.95,wallLength=2.86,thickness=.08,measurementType="n",offset=.75,height=None).new_texture(tw)
room.add_perpendicular_wall(3,distance=.08,wallLength=.9,thickness=.16,measurementType="n",height=None).new_texture(tw)
room.add_perpendicular_wall(3,distance=1.88,wallLength=.9,thickness=.08,measurementType="a",height=None).new_texture(tw)
room.add_perpendicular_wall(3,distance=1.6,wallLength=1.1,thickness=.08,measurementType="a",offset=.95,height=None).new_texture(tw)
room.add_perpendicular_wall(3,distance=2.3,wallLength=1.1,thickness=.08,measurementType="a",offset=.95,height=None).new_texture(tw)
for w in room.walls:
    w.new_texture(tw)
door1=room.add_door(wallNumber=8,wlength=.83,wheight=2.15,wdepth=.1,deltaLength=1.45,handleTexture=handleTexture).new_texture(texDoor)
door1.name="porte1"
door1.new_texture(texDoor)



camera=Camera()

entrance=point(7,1,2)
floorCenter=origin+3.5*Y+5.6*X

sun=Light(origin+100*(5*Z-1*X-4*Y)) # a light
sun.rgbColor=[1,1,1]

livingLamp=Lamp().hooked_on(floorCenter-1.7*Y+2.5*Z).glued_on(ground).add_to_texture(lampFinish)
livingLamp.add_to_texture(lampFinish2) # a light
corridorLamp=Lamp(shadowless=False).hooked_on(origin+2.5*Z+8*X+3.15*Y).glued_on(room).add_to_texture(lampFinish)

#kitchenLamp=Lamp().hooked_on(origin+2.5*Z+2*X+1.5*Y).glued_on(room)
#unseenLamp=Light().hooked_on(floorCenter-1*Y+1.2*Z+2*X).glued_on(ground) # a light
#unseenLamp.color="rgb <1,1,1>"

#light4=Lamp().hooked_on(origin+2.5*Z+2*X+4.5*Y).glued_on(room)

#light6=Light().hooked_on(floorCenter-5.7*Y+2.5*Z+X).glued_on(room) # a light
#light65=Light().hooked_on(floorCenter-5.7*Y+2*Z+X).glued_on(room) # a light
#light7=Light().hooked_on(floorCenter-1*X-5.7*Y+2.5*Z).glued_on(room) # a light
#light8=Light().hooked_on(origin+3*X+.05*Y+2*Z).glued_on(room) # a light




table=Table(1.2,.8,.7,.03).new_texture(tableTexture.copy()).above(origin+4.8*X+1.5*Y).glued_on(room).add_to_texture(tableBump)
table.name="table"
table.add_hook("glass1",table.point(.5,.5,1))
glass1=Glass()
glass2=Glass()
glass3=Glass()
glass1.hooked_on(table).glued_on(table).translate(.1*Y)
glass2.hooked_on(table).glued_on(table).translate(.2*X)
glass3.hooked_on(table).glued_on(table).translate(-.2*X)

chair1=Chair().new_texture(tableTexture.copy()).above(origin+4.5*X+1.87*Y+.4*Z).glued_on(table)
chair1.seat.new_texture(chairSeatTexture)
chair2=chair1.copy()
chair2.above(origin+5*X+1.8*Y+.4*Z).glued_on(table)
chair2=chair1.copy().above(origin+4.5*X+1*Y+.4*Z).glued_on(table).self_rotate(3)
chair2=chair1.copy().above(origin+5*X+1*Y+.4*Z).glued_on(table).self_rotate(3.5)
table.translate(.82*X)
stovePosistionOnFloor=origin+7.50*X+2.3*Y
stove=Stove().glued_on(room).self_rotate(-math.pi/2)
stove.name="stove"
stove.translate(stovePosistionOnFloor-stove.floorPoint)
stove.spacer.texture.enhance(stoveFinish)
#stove.new_texture(stoveTexture)

cabinet=Cabinet().select_hook("hookToFloor").hooked_on(origin)
cabinet.pirotate(Z,-.5).glued_on(room)
pointOnWall4=room.walls[4].insideBaseLine().point(.2,"p")
cabinet.select_hook("backHook").self_gtranslate(pointOnWall4,vec=X).translate(-.04*X)
cabinet.select_hook("backHook").self_gtranslate(pointOnWall4,vec=Y).translate(.3*Y)


camera.projection="orthographic"
camera.projection="perspective"
#camera.location=origin+1.6*X+1.5*Y+1.62*Z
camera.location=entrance-3.6*X+1.8*Y-.3*Z
#camera.location=entrance-3.9*X-10*Y-.3*Z
camera.actors=[room,ground] # what is seen by the camera
#camera.actors=[room.walls]
#camera.actors=[tiling]
#camera.actors=[ls]
#camera.lookAt=origin
camera.lookAt=entrance+1*Y-1.05*Z
#camera.lookAt=origin
camera.angle=1.07
#for light in camera.lights:
#    print(light.povray_string())

camera.quality=0
#print("a la fin",room.floor.texture.smallString)
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
#camera.show # show the photo, ie calls povray. 
#print (globVars.TextureString)
#print(room.texture.smallString)
