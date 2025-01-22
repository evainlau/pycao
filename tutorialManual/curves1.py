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


#bbloc1
ground=plane(Z,origin-Z)
ground.colored("Gray")
curve1=BezierCurve([origin,-X+Y,X+Y,X-Y,-X-Y-.5*Z])
curve1.show() # use default arguments
curve2=Polyline([origin,-X+Y,X+Y,X-Y,-X-Y-.5*Z])
# For the polyline, we don't use the default options
curve2.show(radius=0.1,steps=50,color="Red",color2="Blue")
curve2.translate(2*X+2*Y+0*Z)
#ebloc1

#################################################
#  Now, what you see
#################################################


directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/generatedImages/"+os.path.splitext(base)[0]+".pov"
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.3)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+0*X-1*Y+1*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(camera.hook()+1*X+1*Z) # a light located close to the camera

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
