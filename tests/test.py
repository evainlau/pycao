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



def WoodStud(dimx,dimy,dimz,grainVector=Z,texture=None):
    if texture is None:
        texture=Texture("DMFDarkOak scale .03")
    c=Cube.from_dimensions(dimx,dimy,dimz)
    M=Map.rotational_difference(Z,grainVector)    
    c.new_texture(texture)
    c.texture.move(M)
    return c

def RoundedWoodStud(dimx,dimy,dimz,radius=.005,grainVector=Z,texture=None):
    if texture is None:
        texture=Texture("DMFDarkOak scale .03")
    c=RoundBox.from_dimensions(dimx,dimy,dimz,radius)
    c.new_texture(texture)
    M=Map.rotational_difference(Z,grainVector)
    c.texture.move(M)
    return c

def WoodBoard(xdim,ydim,thickness,xnumber=2,grainVector=Z,texture=None):
    """ 
    returns a board in the xy plane obtained by tiling in the x direction
    """
    if texture is None:
        texture=Texture("DMFDarkOak scale .03")
    c=RoundedWoodStud(xdim,ydim,thickness,radius=.005,grainVector=grainVector,texture=texture)
    return c#Tiling(c,jointWidth=-.0001,jointHeight=0,xnumber=xnumber,ynumber=1,polyline=None)

def PictureFrame(xdim,ydim,thickness,borderWidth,radius=.005):
    l1=RoundedWoodStud(xdim,borderWidth,2*thickness,radius=radius,grainVector=X)
    l3=l1.copy().translate((ydim-borderWidth)*Y)
    l2=RoundedWoodStud(borderWidth,ydim,2*thickness,radius=radius,grainVector=Y)
    l4=l2.copy().translate((xdim-borderWidth)*X)
    plane1=plane.from_3_points(origin,origin+Z,origin+X+Y)
    if plane1.half_space_contains(origin+X):
        plane1.reverse()
    l1.amputed_by(plane1)
    l2.amputed_by(plane1.copy().reverse())
    plane1.translate(l3.point(1,1,1,"ppp")-origin)
    l4.amputed_by(plane1)
    l3.amputed_by(plane1.copy().reverse())
    plane2=plane.from_3_points(origin,origin+Z,origin-X+Y)
    if plane2.half_space_contains(origin+X+Y):
        plane2.reverse()
    plane3=plane2.copy().translate(xdim*X)
    plane2.translate(ydim*Y)
    l2.amputed_by(plane2.copy().reverse())
    l3.amputed_by(plane2)
    l1.amputed_by(plane3.copy().reverse())
    l4.amputed_by(plane3)
    ret=Compound()
    ret.add_list_to_compound([l1,l2,l3,l4])
    ret.add_box("globalBox",Cube(origin,origin+xdim*X+ydim*Y+thickness*Z).box())
    return ret

def FramedGlass(width,height,thickness,borderWidth):
    mape=Map.linear(X,Z,Y)
    border=PictureFrame(width,height,thickness,borderWidth).move(mape)
    glass=Cube(origin,origin+(width-2*borderWidth)*X+(height-2*borderWidth)*Z+.002*Y)
    glass.new_texture("Glass")
    glass.translate(border.center-glass.center)
    ret=Compound()
    ret.add_list_to_compound([["frame",border],["glass",glass]])
    ret.add_box("globalBox",border.box())
    return ret

def CabinetStorey(b0,b1,b2,b3):
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
        ob.add_hook("bottomFrontLeft",ob.point(0,0,0,"ppp"))
        ob.add_hook("bottomFrontRight",ob.point(1,0,0,"ppp"))
    for pair in [[b0,b1],[b1,b2],[b2,b3]]:
        pair[0].select_hook("bottomFrontRight")
        pair[1].select_hook("bottomFrontLeft")
        pair[1].hooked_on(pair[0])
    c=Compound()
    c.add_list_to_compound([["front",b0],["right",b1],["back",b2],["left",b3]])
    d=Cube(b0.point(0,0,0,"ppp"),b1.point(1,0,1,"ppp"))
    #print(b1[0])
    c.add_box("globalBox",d.box())
    return c

def Drawer(dimx,dimy,dimz,thickness):
    print("thickness",dimz-thickness)
    #print("texture in drawer1",texture)
    print("ocals1",locals())
    b0=WoodBoard(dimx,thickness,dimz-thickness,grainVector=X)
    #print("texture in drawer2",WoodBoard.texture)
    b2=b0.copy()
    b1=WoodBoard(dimy,thickness,dimz-thickness,grainVector=X)
    b3=b1.copy()
    c=CabinetStorey(b0,b1,b2,b3)
    b=WoodBoard(dimx,dimy,thickness,grainVector=Y)
    c.above(b)
    ret=Compound()
    ret.add_list_to_compound([b,c])
    return ret





l=Light().translate(3*Z-Y)
floor=FramedGlass(.4,.6,.02,.07).translate(.1*Z).light_level(1)
#floor=PictureFrame(xdim=.4,ydim=.3,width=.05,thickness=.01,radius=.005)
#print("now woodb")
#floor=WoodBoard(.2,.4,thickness=.01,grainVector=X).named("Woodboard")
#floor2=RoundedWoodStud(.2,.4,.01,grainVector=X).named("RoundedWS")
#floor=Woo(.2,.2,.4)


camera=Camera()
camera.projection="perspective"
camera.filmAllActors=False
camera.location=origin-0*X-1*Y+1*Z
l=Light().translate(2*Y+15*Z)
#camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"
#camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
#camera.actors=[table.c13,table.c12,table.s1] # what is seen by the camera#\\
camera.actors=[floor,ground] # what is seen by the camera
#ground.visibility=0
camera.lookAt=floor.center
camera.zoom(1)


camera.angle=0.84
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
