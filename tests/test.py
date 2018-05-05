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

def WoodStud(dimx,dimy,dimz,grainVector):
    c=Cube.from_dimensions(dimx,dimy,dimz)
    M=Map.rotational_difference(Y,grainVector)
    c.makeup(Texture("T_Wood3").move(M))
    return c

def RoundedWoodStud(dimx,dimy,dimz,radius=.005,grainVector=Z):
    c=RoundBox.from_dimensions(dimx,dimy,dimz,radius)
    M=Map.rotational_difference(Y,grainVector)
    c.makeup(Texture("T_Wood3").move(M))
    return c



def WoodBoard(xdim,ydim,thickness,xnumber,grainVector):
    c=RoundedWoodStud(xdim,ydim,thickness,.005)
    M=Map.rotational_difference(Y,grainVector)
    c.makeup(Texture("T_Wood3").move(M))
    return Tiling(c,jointWidth=-.0001,jointHeight=0,xnumber=xnumber,ynumber=1,polyline=None)

def PictureFrame(xdim,ydim,width,thickness,radius=.005):
    l1=RoundedWoodStud(xdim,width,2*thickness,radius=radius,grainVector=X)
    l3=l1.copy().translate((ydim-width)*Y)
    l2=RoundedWoodStud(width,ydim,2*thickness,radius=radius,grainVector=Y)
    l4=l2.copy().translate((xdim-width)*X)
    ret=Compound()
    ret.add_list_to_compound([l1,l2,l3,l4])
    return ret

def cabinetStorey(b0,b1,b2,b3):
    """
    creates a storey for a cabinet from 4 boeards. The 4 boards are in the (x,z) plane and parallel
    and the outside face of the board is oriented towards the negative y. 
    This function gives the right orientation to the 4 boards and returns a compound with 4 panels 
    called front,irght,back,left, and a box. Each board must have a box for the computations to occur. 
    """
    b0.named("b0")
    b1.rotate(Z,math.pi/2).named("b1")
    b2.rotate(Z,math.pi).named("b2")
    b3.rotate(Z,-math.pi/2).named("b3")
    for ob in [b0,b1,b2,b3]:
        ob.add_handle("bottomFrontLeft",ob.point(0,0,0,"ppp"))
        ob.add_handle("bottomFrontRight",ob.point(1,0,0,"ppp"))
    for pair in [[b0,b1],[b1,b2],[b2,b3]]:
        pair[0].select_handle("bottomFrontRight")
        pair[1].select_handle("bottomFrontLeft")
        pair[1].hooked_on(pair[0])
    c=Compound()
    c.add_list_to_compound([["front",b0],["right",b1],["back",b2],["left",b3]])
    d=Cube(b0.point(0,0,0,"ppp"),b1.point(1,0,1,"ppp"))
    c.add_box("globalBox",d.box())
    return c

#b0=Cube.from_dimensions(1,.02,.5)
b0=WoodBoard(xdim=1,ydim=.5,thickness=.01,xnumber=1,grainVector=Z).move(Map.linear(X,Z,Y))
b1=b0.copy()
b2=b0.copy()
b3=b0.copy()
floor=cabinetStorey(b0,b1,b2,b3)#PictureFrame(.6,.4,.07,.02)

camera=Camera()
camera.projection="perspective"
camera.filmAllActors=False
camera.location=origin-0*X-4*Y+3*Z
l=Light().translate(2*Y+15*Z)
#camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
#camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
#camera.actors=[table.c13,table.c12,table.s1] # what is seen by the camera#\\
camera.actors=[floor,ground] # what is seen by the camera
#ground.visibility=0
camera.lookAt=origin
camera.zoom(1)


camera.angle=0.84
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
