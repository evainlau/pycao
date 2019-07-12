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
pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core"

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
   curve=PiecewiseCurve.from_interpolation([origin+X-Y,.5*X,+2*Y,-.5*X],speedConstants=[.24,.24],closeCurve=True).show()
   Lathe.fromPiecewiseCurve(curve).rgbed(.8,.4,.4,.5)

   curve2=Polyline([origin+X+2*Y,.5*Y,.5*Y+.5*X])
   Lathe(curve2).colored("Bronze").translate(4*X-2*Y)
   Plane(Z,origin-1.5*Z).colored("Gray")
  # The curve is assumed to have points of the form [0,y,z]



#################################################
#  Now, what you see
#################################################

camera.file="curvesLathe.pov" # A name for the povray file that will be generated. Must end with .pov
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.25)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+1.3*X-5.2*Y+2.2*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(camera.hook()+1*Y+2*Z) # a light located close to the camera

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
