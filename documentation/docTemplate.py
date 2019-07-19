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
light=Light().hooked_on(camera.hook()+3*X) # a light located close to the camera                                                                            

#######################################

"""
                SCENE DESCRIPTION
"""

#bbloc1 

#ebloc1



camera.hooked_on(origin-.6*Y+1*Z)  # the positive y are in front of us because the camera is located in negative Y and we look at
camera.lookAt=origin # look at the center of cyl
camera.actors=[]

camera.povraypath=pycaoDir+"/../images/" # where you put your images,photos for the textures
camera.zoom(1.5)
camera.imageHeight=600 # in pixels
camera.imageWidth=600 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
fileNameNoSuffix=os.path.splitext(base)[0]
camera.file=directory+"/docPictures/"+fileNameNoSuffix+".pov"

camera.shoot
camera.pov_to_png

#################################################
#  Now, what you see
#################################################

