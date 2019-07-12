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
light=Light().hooked_on(camera.hook()+3*X-Z) # a light located close to the camera
light.glued_on(camera) # the light will follow the camera, so that you will get light on your objects


#######################################

"""
                SCENE DESCRIPTION
"""


if 1>0:
    g=plane(Z,origin).colored("Grey")
    cyl=Cylinder(origin,origin+1.5*Z,.5).colored("Yellow")
    myCube=Cube(1,1,1).colored("Brown").above(cyl)
    
camera.filmAllActors=False
camera.file="cubeOverCyl.pov"
camera.location=origin-4.3*Y+2.*Z-2*X
camera.zoom(.15)
camera.lookAt=origin
camera.filmAllActors=True
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.shoot
camera.pov_to_png



#################################################
#  Now, what you see
#################################################


camera.hooked_on(origin-4*Y+2*Z)  # the positive y are in front of us because the camera is located in negative Y and we look at  a point close to the origin
camera.lookAt=cyl.point(.5,.5,.5) # look at the center of cyl
# uncomment the following line if you want to see all objects without filling manually
# the previous list camera.actors. It will override the previous line.
#camera.filmAllActors=True # overrides the camera.actors list
camera.file="pycaoOutput.pov" # A name for the povray file that will be generated. Must end with .pov
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.15)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
#camera.show # show the photo, ie calls povray. 
#camera.show_without_viewer # if you want only the photo but not the graphical interface, u
