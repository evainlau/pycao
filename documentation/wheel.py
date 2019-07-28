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






w=RearWheel()
p=plane(Z,origin-(w.tyre.externalRadius+.02)*Z).colored("Bronze")
#Washer(origin-0.015*Y,origin+0.015*Y,.6,.7)

directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera=Camera().hooked_on(origin+1*(-5*Y-X+3*Z))
l=Light().hooked_on(origin+10*(-2*Y-0*X+6*Z))
camera.file=directory+"/generatedImages/"+os.path.splitext(base)[0]+".pov"
#camera.filmAllActors=True
camera.actors=[p,w]
camera.zoom(3.6)
camera.shoot.pov_to_png
