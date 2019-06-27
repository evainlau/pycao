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





# a plane represented graphically as a half space 
ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
ground.colored('Gray') # The possible colors are the colors described in colors.inc in povray or a rgb color as in the exemple below. 

wall=Cube(2,.5,1.5).colored('Brown') # A wall given by a cube of prescribed dimension
myPoint=wall.point(0.5,0.5,0) # this is the point in the middle ( coordinates=.5)  X and Y, and below (coordinate 0 for Z). 
wall.add_hook("bottom",myPoint) # A hook with name "bottom" is added to the wall and is selected as the active hook. of the wall. 
wall.hooked_on(origin) # the wall is moved by moving its active hook to the origin, ie. the bottom of the wall goes to the origin


# a vertical cylinder
cyl=Cylinder(start=origin+2*X,end=origin+2*X+Z,radius=0.5).colored('SpicyPink')

axis=Segment(point(4,0,0),point(4,0,1))
#an infinite cylinder of radius 0.5
cyl2=ICylinder(axis,0.5).new_texture("pigment { brick Black Green brick_size 2 mortar 0.2 }")


s=Sphere(point(6,0,0),1)
s.rgbed(1.5,0.5,0.5,1)# three rgb colors. The fourth entry of the rgbed function is facultative, giving transparency




#################################################
#  Now, what you see
#################################################


camera.hooked_on(origin-4*Y+2*Z)  # the positive y are in front of us because the camera is located in negative Y and we look at  a point close to the origin
camera.lookAt=cyl.point(.5,.5,.5) # look at the center of cyl
camera.actors=[wall,ground,cyl,cyl2,s] # what is seen by the camera
# uncomment the following line if you want to see all objects. It will override the previous line.
#camera.filmAllActors=True # overrides the camera.actors list
camera.file="pycaoOutput.pov" # A name for the povray file that will be generated. Must end with .pov
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(0.15)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.show # show the photo, ie calls povray. 
#camera.show_without_viewer # if you want only the photo but not the graphical interface, u
