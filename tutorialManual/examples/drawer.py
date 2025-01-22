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
thisFileAbsName=os.path.abspath(__file__)
pycaoDir=os.path.dirname(thisFileAbsName)+"/../../core"

#


"""
                MODULES IMPORT
"""


import sys
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
ground.textured(Texture.from_photo("woodFloor1.png",symmetric=True).scale(2.6,2.6,1))
ground.name="plan"



feetheight=.1
feetSize=.1

## the front face and the drawer , 
up=FramedGlass(width=.5,height=.4,thickness=.02,borderWidth=.06)
bot=FramedDrawer(width=.5,height=.3,thickness=.02,borderWidth=.06,openingAmount=1.15)
up.above(bot)
frontFace=Compound()
frontFace.add_list_to_compound([["up",up],["bot",bot]])
## a box containing the front face:
f=FrameBox(up.box().points+bot.box().points)
frontFace.add_box("globalBox",f)
dim=f.dimensions
### now the part behind the front face, using the dimension of the box. 
b1=WoodStud(dimx=.3,dimy=dim[1],dimz=dim[2],grainVector=Z)
b2=WoodStud(dimx=dim[0],dimy=dim[1],dimz=dim[2],grainVector=Z)
b3=b1.clone()
mainPart=CabinetStorey(frontFace,b1,b2,b3)
dim=mainPart.dimensions
#now a support for what we drew
support=WoodStud(dim[0]+.015,dim[1]+.015,.01)
mainPart.above(support)
# and atop
top=FramedStub(width=dim[0]+.015,height=dim[1]+.015,thickness=.01,borderWidth=.07)
top2=FramedStub(width=dim[0]+.015,height=dim[1]+.015,thickness=.01,borderWidth=.07)
top.parallel_to(Z)
top.activeBox.reorder()
top.above(mainPart)
# and feet below the support
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
bottom=feet.box().point(.5,.5,0)
cabinet.translate(origin-bottom)

#actor=Cabinet().pirotate(Z,0.6).hooked_on(origin)
#actor=Cabinet().hooked_on(origin)
actor=cabinet


camera=Camera()
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/../generatedImages/"+os.path.splitext(base)[0]+".pov"
camera.projection="perspective"
camera.filmAllActors=False
camera.location=origin-0.8*X-1.*Y+1*Z
l1=Light(origin-4*Y+10*Z-3*X)
l2=Light(origin-4*Y+10*Z-3.5*X)
camera.actors=[actor,ground]#,floor2]#,ground] # what is seen by the camera
#ground.visibility=0
#camera.actors=[top2.frame]
camera.lookAt=actor.center#origin
#camera.lookAt=origin
camera.zoom(.85)

camera.quality=11
camera.povraypath=pycaoDir+"/../images/"
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 

