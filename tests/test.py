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

feetheight=.1
feetSize=.1
up=FramedGlass(width=.5,height=.4,thickness=.02,borderWidth=.06)
bot=FramedDrawer(width=.5,height=.3,thickness=.02,borderWidth=.06,openingAmount=0)
up.above(bot)
frontFace=Compound()
frontFace.add_list_to_compound([["up",up],["bot",bot]])
f=FrameBox(up.box().points+bot.box().points)
frontFace.add_box("globalBox",f)
dim=f.dimensions
b1=WoodStud(dimx=.3,dimy=dim[1],dimz=dim[2],grainVector=Z)
#pourquoi ne marche pas avec *dim ?
b2=WoodStud(dimx=dim[0],dimy=dim[1],dimz=dim[2],grainVector=Z)
b3=b1.copy()
mainPart=CabinetStorey(frontFace,b1,b2,b3)
dim=mainPart.dimensions
support=WoodStud(dim[0]+.015,dim[1]+.015,.01)
mainPart.above(support)
top=FramedStub(width=dim[0]+.015,height=dim[1]+.015,thickness=.01,borderWidth=.07)
top.parallel_to(Z)
top.activeBox.reorder()
top.above(mainPart)
#dimx=.3,dimy=dim[1],dimz=dim[2],

feet=WoodStud(dim[0],dim[1],2*feetheight)
toCut1=RoundedWoodStud((1-2*feetSize)*dim[0],dim[1]+1,2*feetheight+.001,radius=.4*feetheight)
toCut1.translate(feet.center-toCut1.center)
toCut2=RoundedWoodStud(dim[0]+1,(1-2*feetSize)*dim[1],2*feetheight+.001,radius=.4*feetheight)
toCut2.translate(feet.center-toCut2.center)
toCut3=plane.from_coeffs(0,0,1,-feetheight)
feet.amputed_by([toCut1,toCut2,toCut3])
feet.below(support)


cabinet=Compound()
cabinet.add_list_to_compound([mainPart,support,feet,top])
cabinet.add_box("mp",mainPart.box())
actor=Cabinet().hooked_on(origin).light_level(2)#FramedStub()
#actor=actor.feet
#print(top.frame.box())
#print(top.stub.box())


camera=Camera()
camera.projection="perspective"
camera.filmAllActors=False
camera.location=origin-0*X-1*Y+1*Z
l=Light(origin-2*Y+15*Z)
#camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
#camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
#camera.actors=[table.c13,table.c12,table.s1] # what is seen by the camera#\\
camera.actors=[actor,ground]#,floor2]#,ground] # what is seen by the camera
#ground.visibility=0
camera.lookAt=actor.center#origin
camera.zoom(1)


camera.angle=0.84
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
#print(actor.center)
#print(actor.box())
#print(actor.box().point(0,0,1,"ppp"))
