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



pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao/core"
##pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/core"
import os
thisFileAbsName=os.path.abspath(__file__)
pycaoDir=os.path.dirname(thisFileAbsName)+"/../core"

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
from bikelibrary import RearWheel
from bikelibrary import FrontWheel



class FronteWheel(Compound):
    """
    A class for Front wheels ie. with a rim, a hub, a tyre, and spokes, but no cassette 

    Constructor
    FrontWheel(tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.1,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=32,spokeRadius=0.0018,spokeColor='Black'
    ,rimOuterRadius=0.345,rimInnerRadius=0.320, axisRadius=.005)
    """
    def __init__(self,tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.1,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=26,spokeRadius=0.0018,spokeColor='Black'
                 ,rimOuterRadius=0.345,rimInnerRadius=0.320,axisRadius=.005):

        
        # tyre and rim
        tyre=Torus(tyreExteriorDiameter/2,tyreInternalRadius,Y,origin)
        rim=Washer(origin-0.015*Y,origin+0.015*Y,rimOuterRadius,rimInnerRadius)
        tyre.colored(tyreColor)
        rim.rgbed(1,0,0)

        # the axis
        wheelPhysicalAxis=Cylinder(tyre.center-(hubWidth*.5+.02)*Y,tyre.center+(hubWidth*.5+.02)*Y,axisRadius).colored("Red")
        #hub
        hub=Cylinder(origin-hubWidth/2*Y,origin+hubWidth/2*Y,hubInternalRadius)
        hub.colored(hubColor)
        plaque1=Cylinder(origin,origin+0.0002*Y,hubExternalRadius)
        plaque1.colored(hubColor)
        #print(plaque1.box())
        #print(hub.box())
        plaque1.against(hub,Y,Y,X,X)
        plaque2=plaque1.clone()
        plaque2.against(hub,-Y,-Y,X,X)
        self.slaves=[["tyre",tyre],rim,plaque1,plaque2,["hub",hub],["axis",wheelPhysicalAxis]]
        

        # firstLeftSpoke
        spokeInit=plaque1.point(0.5,0.5,0.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),math.pi*4/numberOfSpokes)
        leftSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        leftSpoke.colored(spokeColor)

        # firstRightspoke
        spokeInit=plaque2.point(0.5,0.5,.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),-math.pi*4/numberOfSpokes)
        rightSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        rightSpoke.colored(spokeColor)

        # otherSpokes via rotation.
        for i in range(int(numberOfSpokes/2)):
            spoke1=leftSpoke.clone()
            self.slaves.append(spoke1.rotate(tyre.axis(),4*math.pi/numberOfSpokes*i))
            spoke2=rightSpoke.clone()
            self.slaves.append(spoke2.rotate(tyre.axis(),4*math.pi/numberOfSpokes*(i+0.5)))
        Compound.__init__(self,self.slaves)
        b=FrameBox([tyre.point(0,0,0),tyre.point(1,1,1),hub.point(0,0,0),hub.point(1,1,1)])
        self.add_box("wheel",b)
        self.add_axis("wheelAxis",hub.axis())




#w=RearWheel()
#w.cassette.textured("Metal")
#p=plane(Z,origin-(w.tyre.externalRadius+.02)*Z).colored("Bronze")
#Washer(origin-0.015*Y,origin+0.015*Y,.6,.7)

directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera=Camera().hooked_on(origin-1.5*(-5*Y-5*X-5*Z))
l=Light().hooked_on(origin+10*(-2*Y-0*X+6*Z))
camera.file=directory+"/"+os.path.splitext(base)[0]+".scad"
camera.file=directory+"/"+os.path.splitext(base)[0]+".pov"
#camera.filmAllActors=True
p=plane(Z,origin).rgbed(1,1,1)
c=Cube(1,1,1).rgbed(1,0,0)
d=Cube(1,1,1).rgbed(1,0,0)
c.clone().translate(X).glued_on(d).rgbed(0,1,0)
c.clone().translate(2*X).glued_on(d)
c.clone().translate(3*X).glued_on(d)
c.clone().translate(Y).glued_on(d)
c.clone().translate(Z).glued_on(d).rgbed(0,0,1)
q=QuadraticEquation(xx=1,yy=1)
camera.actors=[p,d]
camera.zoom(0.6)
#camera.shoot.pov_to_png
camera.technology="povray"
#camera.technology="scad"
camera.quality=2
camera.shoot
camera.show
