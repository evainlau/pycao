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
from material import *
from architecturelibrary import *

"""
                SCENE DESCRIPTION
"""

# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('DarkGreen') # The possible colors are the colors described in colors.inc in povray or a rgb color. 
ground.name="plan"

#wall=Room(Polyline([origin,X,X+Y,Y,-2*X,-Y])).colored("Yellow")





l=Light(origin+3*Z-Y)
#floor=Drawer(dimx=.4,dimy=.5,dimz=.1,thickness=.03)

#floor=FramedGlass(.4,.6,.02,.07).translate(.1*Z).light_level(1)
#floor=PictureFrame(width=.4,height=.3,thickness=.01,borderWidth=.05,radius=.005)

#floor.add_drawer()

up=FramedGlass(width=.5,height=.6,thickness=.02,borderWidth=.06)
bot=FramedDrawer(width=.5,height=.3,thickness=.02,borderWidth=.06,openingAmount=0)
up.above(bot)
floor=Compound()
floor.add_list_to_compound([["up",up],["boy",bot]])
#mape=Map.linear(X,Z,14*Y)
#floor.move(mape)
#floor.rotate(X,math.pi/2)
#floor=RoundedWoodStud(.4,.6,.03,radius=.003,grainVector=Y).named("l2")
#floor=WoodStud(dimx=.4,dimy=.1,dimz=.5,grainVector=Y,texture=None).named("f")
#floor=RoundedWoodStud(dimx=.4,dimy=.3,dimz=.5,grainVector=Z,texture=None)#.rotate(X,math.pi/2)
#floor2=floor.copy().named("f2").translate(.4*X)
#mape=Map.rotation(X,math.pi/2)
#floor.move(mape)
#floor=WoodBoard(.2,.4,thickness=.01,grainVector=X).named("Woodboard")
#floor2=RoundedWoodStud(.2,.4,.01,grainVector=X).named("RoundedWS")
#floor=Woo(.2,.2,.4)

floor=Compound().add_box("mybox",Cube(.2,.42,.32).box())
floor2=floor.copy().translate(.5*X)
#print (floor.__dict__)
#delattr( floor,"box")
#floor.add_box("newbox",floor.box())
#floor.move(Map.flipXY())
print floor.box()
print "was avt"
print(floor.dicobox.mybox)
print(floor.dicobox.mybox.points)
floor.dicobox.mybox.axisPermutation(2,1,3)
print(floor.dicobox.mybox)
print(floor.dicobox.mybox.points)
floor.dicobox.mybox.reorder()
print floor.box()
print "was apres"
floor.show_box().translate(-.5*X)
floor2.show_box()


camera=Camera()
camera.projection="perspective"
camera.filmAllActors=False
camera.location=origin-0*X-1*Y+1*Z
l=Light(origin+2*Y+15*Z)
#camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
#camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
#camera.actors=[table.c13,table.c12,table.s1] # what is seen by the camera#\\
camera.actors=[floor,floor2]#,ground] # what is seen by the camera
#ground.visibility=0
camera.lookAt=origin
camera.zoom(1)


camera.angle=0.84
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
#camera.show # show the photo, ie calls povray. 

