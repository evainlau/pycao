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



pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core/"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core/"

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


plane(Z,origin).colored("Gray")
cadran=Cylinder(origin,origin+.02*Z+.002*X,.2).colored("Bronze")
mark=Cube(origin,origin+.02*X+.01*Y+.001*Z).colored("Blue")
mark.add_axis("vectorToCenter",mark.boxline(x=None,y=.5,z=.5))
mark.add_hook("pointToAttach",mark.point(.5,.5,0))
for i in range(12):
    p=cadran.cylpoint(r=.02,w=1./12*i,s=1,frame="np")
    q=cadran.cylpoint(r=0,w=i/12.,s=1)
    mark.clone().parallel_to(q-p).hooked_on(p).colored("Black")


#################################################
#  Now, what you see
#################################################


camera.file="watch.pov" # A name for the povray file that will be generated. Must end with .pov
camera.zoom(3.45)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin 

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+0*X-1*Y+3*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(camera.hook()+1*X+1*Z) # a light located close to the camera

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
#camera.show_without_viewer # if you want only the photo but not the graphical interface
