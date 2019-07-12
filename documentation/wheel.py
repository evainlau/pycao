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
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/core"

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


class FrontWheel(Compound):
    """
    A class for Front wheels with a rim, a hub, a tyre, and spokes. 

    Constructor
    FrontWheel(tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.3,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=32,spokeRadius=0.0018,spokeColor='Black'
    ,rimOuterRadius=0.345,rimInnerRadius=0.320)
    """
    def __init__(self,tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.3,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=32,spokeRadius=0.0018,spokeColor='Black'
    ,rimOuterRadius=0.345,rimInnerRadius=0.320):

        # tyre and rim
        tyre=Torus(tyreExteriorDiameter/2,tyreInternalRadius,Y,origin)
        rim=Washer(origin-0.015*Y,origin+0.015*Y,rimOuterRadius,rimInnerRadius)
        tyre.color=tyreColor
        rim.color=rimColor

        #hub
        hub=Cylinder(origin-hubWidth/2*Y,origin+hubWidth/2*Y,hubInternalRadius)
        hub.color=hubColor
        plaque1=Cylinder(origin,origin+0.0002*Y,hubExternalRadius)
        plaque1.color=hubColor
        plaque1.against(hub,Y,Y,X,X)
        plaque2=plaque1.clone()
        plaque2.against(hub,-Y,-Y,X,X)

        self.slaves=[tyre,rim,plaque1,plaque2,["hub",hub]]

        # firstLeftSpoke
        spokeInit=plaque1.point(0.5,0.5,0.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),math.pi*4/numberOfSpokes)
        leftSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        leftSpoke.color=spokeColor

        # firstRightspoke
        spokeInit=plaque2.point(0.5,0.5,.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),-math.pi*4/numberOfSpokes)
        rightSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        rightSpoke.color=spokeColor

        # otherSpokes via rotation.
        for i in range(numberOfSpokes/2):
            spoke1=leftSpoke.clone()
            self.slaves.append(spoke1.rotate(tyre.axis(),4*math.pi/numberOfSpokes*i))
            spoke2=rightSpoke.clone()
            self.slaves.append(spoke2.rotate(tyre.axis(),4*math.pi/numberOfSpokes*(i+0.5)))

        self.build_from_slaves()




