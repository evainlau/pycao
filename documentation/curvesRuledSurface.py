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



#pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core"
import os
thisFileAbsName=os.path.abspath(__file__)
pycaoDir=os.path.dirname(thisFileAbsName)+"/../core"

import sys
sys.path.append(pycaoDir)


"""
                MODULES IMPORT
"""


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




###############################
# By default, lights you will append in the file  are appended to existing cameras. So probably 
# you want to leave the first line defining the camera at the beginning of the file


camera=Camera()

#######################################

"""
                SCENE DESCRIPTION
"""
if 1>0:   
   ground=plane(Z,origin-Z)
   ground.colored("Gray")

   #Filling a Bezier curve in Red
   curve0=BezierCurve([origin,-X,+Y,+X,origin])
   curveFilling=RuledSurface.fromCurveFilling(curve0,quality=2)
   curveFilling.colored("Red")
   curveFilling.translate(-2*X)

   # The green join
   curve1=PiecewiseCurve.from_interpolation([origin,-X,+Y,+X,origin])
   # Remark the non smooth join.
   curve2=curve1.clone().translate(1.5*Z).named("Courbe2")
   tube=RuledSurface(curve1,curve2,quality=8)
   tube.colored("HuntersGreen")

   #The violet join
   # Now, for curve3, to get a smmooth join, we suppress one point in comparison to curve 1,
   # and we add the option closeCurve=True.
   curve3=PiecewiseCurve.from_interpolation([origin+3*X,-X,+Y,+X],closeCurve=True)
   curve4=curve3.clone().translate(1.5*Z)
   def g(t):
      return (t+0.35) %1
   curve3.reparametrize(g)
   tubeWithRotatedBottom=RuledSurface.fromJoinAndCaps(curve3,curve4,quality=5)
   tubeWithRotatedBottom.colored("Violet")






#################################################
#  Now, what you see
#################################################

camera.file="curvesRuledSurfaces.pov" # A name for the povray file that will be generated. Must end with .pov
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.3)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin+.2*Z+.5*X # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+0*X-2*Y+2*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(camera.hook()+1*X+1*Z) # a light located close to the camera

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
