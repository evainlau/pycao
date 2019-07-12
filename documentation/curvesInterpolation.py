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



# The spheres for the 4 points prescribed
#greenSpheresOnControlPoints=[ Sphere(cp,.05).colored("Green") for cp in controlPoints]




#################################################
#  Now, what you see
#################################################

camera.file="pycaoOutput.pov" # A name for the povray file that will be generated. Must end with .pov
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.1)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin+2.5*X+1.7*Y # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+2.5*X+1.5*Y+2*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(camera.hook()+1*X+1*Z) # a light located close to the camera

#camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
#camera.pov_to_png # show the photo, ie calls povray. 


ground=plane(Z,origin)
ground.colored("Gray")

if 1>0:
    controlPoints=([origin+.1*Z,X,Y,-X])
    curve1=PiecewiseCurve.from_interpolation(controlPoints).show(radius=0.03)# color Yellow 
    curve2=PiecewiseCurve.from_interpolation(controlPoints,speedConstants=[.24,.24],closeCurve=True).show(radius=0.03,color='SpicyPink').translate(-2*Y+X)
    curve3=PiecewiseCurve.from_interpolation(controlPoints,closeCurve=True).show(radius=0.03,color='Blue').translate(2.2*X) # speedConstants=[.45,.45]  by default
    curve4=PiecewiseCurve.from_interpolation(controlPoints,speedConstants=[1.5,1.5],closeCurve=True).show(radius=0.03,color='Violet').translate(2*Y+2.2*X)
    curve5=PiecewiseCurve.from_interpolation(controlPoints,speedConstants=[3,3],closeCurve=True).show(radius=0.03,color='Bronze').translate(4*Y-.5*X)
    curve6=PiecewiseCurve.from_interpolation(controlPoints,speedConstants=[4,4],closeCurve=True).show(radius=0.03,color='Red').translate(5*Y+2.5*X)
    # In the following line, the curve has 4 points + one point added by Pycao to close the curve, so the speed vectors have 5 entries
    curve7=PiecewiseCurve.from_interpolation(controlPoints,approachSpeeds=[2,2,2,2,2],leavingSpeeds=[0.4]*5,closeCurve=True).show(radius=0.03,color='Green').translate(2*Y+6*X)


directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"


#curve=PiecewiseCurve.from_interpolation(controlPoints,speedConstants=[.6,.6],closeCurve=True).show(radius=0.03)

#curve=PiecewiseCurve.from_interpolation(controlPoints,speedConstants=[2,2],closeCurve=True).show(radius=0.03)
camera.shoot
camera.pov_to_png

