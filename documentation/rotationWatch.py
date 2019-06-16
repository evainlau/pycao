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



#pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit/distributed"
pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/distributed"

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





# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('SeaGreen') # The possible colors are the colors described in colors.inc in povray or a rgb color as in the exemple below. 

clock=Cylinder(start=origin, end=origin+.03*Z,radius=.21).colored("Gray")
blueSphere=Sphere(origin+.2*X+.2*Y,.03).colored("Blue")
pinkSphere=Sphere(origin-.3*X+.1*Y,.03).colored("Pink")
top=clock.point(.5,.5,1)
clock.add_hook("top",top+.002*Z)
smallWatchHand=Cube(.12,.02,.001).colored("Red").add_axis("axisOfRotation",line(origin,origin+Z))
smallWatchHand.add_hook("end",smallWatchHand.point(1,0,0))
smallWatchHand.add_hook("centerOfRotation",smallWatchHand.point(0,0.5,0)).hooked_on(clock)
smallWatchHand.add_axis("along",line(smallWatchHand.hook("centerOfRotation"),X))
#smallWatchHand.hooked_on(top+.001*Z)
longWatchHand=Cube(.005,.16,.001).rgbed(.1,.6,.3).add_axis("axisOfRotation",line(origin,origin+Z))
longWatchHand.add_hook("centerOfRotation",longWatchHand.point(.5,0,0)).hooked_on(smallWatchHand.hook("centerOfRotation")+.002*Z)
longWatchHand.hooked_on(smallWatchHand.hook()+.003*Z)
longWatchHand.add_axis("along",line(origin,origin+Y))



camera.hooked_on(origin-.6*Y+1*Z)  # the positive y are in front of us because the camera is located in negative Y and we look at
camera.lookAt=origin # look at the center of cyl
camera.actors=[ground,clock,top,smallWatchHand,longWatchHand,blueSphere,pinkSphere] # what is seen by the camera
#camera.actors=[longWatchHand]
camera.file="pycaoOutput.pov" # A name for the povray file that will be generated. Must end with .pov
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(1.5)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene

light=Light().hooked_on(camera.hook()+3*X) # a light located close to the camera                                                                            
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file

if 1>0:
    camera.file="rotationInitial.pov"
    camera.shoot
    camera.show
    smallWatchHand.parallel_to(longWatchHand,fixed=smallWatchHand.hook())
    camera.file="rotationParallel1.pov"
    camera.shoot
    camera.show
    longWatchHand.parallel_to(blueSphere.center-pinkSphere.center,fixed=longWatchHand.hook())
    camera.file="rotationParallel2.pov"
    camera.shoot
    camera.show
    smallWatchHand.select_axis("axisOfRotation")
    smallWatchHand.select_hook("end")
    smallWatchHand.self_grotate(blueSphere.center)
    camera.file="rotationGrotate.pov"
    camera.shoot
    camera.show
#################################################
#  Now, what you see
#################################################

