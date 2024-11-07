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
ground=plane(Z,origin-.01*Z) # a plane with normal the vector Z=vector(0,0,1) containing the origin
#ground.textured(Texture.from_photo("woodFloor1.png",symmetric=True).scale(2.6,2.6,1))
ground.colored("Grey")
ground.name="plan"

length=.2
width=0.04
height=0.02
tourillonRadius=0.005


## the front face and the drawer , 
latte=Cube(length,width,height).colored("Red")
latte.add_hook("percage1haut",latte.point(.5*width,.5,1,"app"))
latte.add_hook("percage1bas",latte.point(.5*width,.5,0,"app"))
latte.add_hook("percage2haut",latte.point(.5*width,.5,1,"npp"))
latte.add_hook("percage2bas",latte.point(.5*width,.5,0,"npp"))
latte.add_hook("hcut1",latte.point(width,.5,1,"app"))
latte.add_hook("hcut2",latte.point(width,.5,1,"npp"))
plane1=plane(X,latte.hook("hcut1"))
plane2=plane(-X,latte.hook("hcut2"))
plane3=plane(-Z,latte.point(.5,.5,.5,"ppp"))
toCut1=plane1.intersected_by(plane3).colored("Green")
toCut2=plane2.intersected_by(plane3).colored("Green")
tourillon1=Cylinder(start=origin-.001*Z,end=origin+height*1.001*Z,radius=tourillonRadius).colored("Yellow")
tourillon1.add_hook("bottomPoint",tourillon1.point(.5,.5,.0,"ppa"))
tourillon1.add_hook("topPoint",tourillon1.point(.5,.5,.001,"ppn"))
tourillon2=tourillon1.clone()
tourillon1.hooked_on(latte.hook("percage1haut"))

tourillon2.hooked_on(latte.hook("percage2haut"))
latte.amputed_by(toCut1)
latte.amputed_by(toCut2)
latte.amputed_by(tourillon1)
latte.amputed_by(tourillon2)
latte2=latte.clone().colored("Pink")
latte3=latte.clone().colored("Brown")
latte2.pirotate(X,1)
latte2.pirotate(Z,.5)
latte2.gtranslate(Z,latte2.hook("percage1haut"),latte.hook("percage1bas"))
latte4=latte2.clone().colored("Blue")
latte4.translate(-latte4.hook("percage1haut")+latte.hook("percage2bas"))
latte3.translate(latte4.hook("percage2haut")-latte3.hook("percage2bas"))

tourillon3=tourillon1.clone()
tourillon4=tourillon1.clone()



#actor=Cabinet().pirotate(Z,0.6).hooked_on(origin)
#actor=Cabinet().hooked_on(origin)


camera=Camera()
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/"+os.path.splitext(base)[0]+".pov"
camera.projection="perspective"
camera.filmAllActors=False
camera.location=origin-0.8*X-1.*Y+1*Z
l1=Light(origin-4*Y+10*Z-3*X)
l2=Light(origin-4*Y+10*Z-3.5*X)
camera.actors=[latte,latte2,latte3,latte4,tourillon1,tourillon2,ground]#,floor2]#,ground] # what is seen by the camera
#camera.actors=[latte4,latte]
#camera.actors=[tourillon1]#,floor2]#,ground] # what is seen by the camera
#ground.visibility=0
#camera.actors=[top2.frame]
camera.lookAt=latte.dicohook.hcut1
camera.lookAt=latte4.hook("percage1haut")
#camera.lookAt=origin
camera.zoom(0.55)

camera.quality=11
camera.povraypath=pycaoDir+"/../images/"
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
#camera.pov_to_png # show the photo, ie calls povray. 
camera.show
