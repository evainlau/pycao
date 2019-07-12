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



#pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core"
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





# a plane represented graphically as a half space 
#ground=plane(Z,origin) # a plane with normal the vector Z=vector(0,0,1) containing the origin
#ground.colored('SeaGreen') # The possible colors are the colors described in colors.inc in povray or a rgb color as in the exemple below. 


if 1>0:
    g=plane(Z,origin-Z).colored("Grey")
    c=Cube(1,1,1).colored("Red")
    d=Cube(2,2,2)
    d.translate(2,0,0).colored("Yellow")
    e=Cylinder(start=origin,end=origin+3*X,radius=0.1)
    o=Compound([c,["cube",d],["cylinder",e]]).colored("Green") # override all the individual colors
    o.cylinder.rotate(Y,1.57) # the Cylinder was horizontal, this instruction puts it vertically

camera=Camera()
camera.file="parentCompound.pov"
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
camera.filmAllActors=True
#camera.actors=[o,g]
camera.zoom(0.4)
camera.lookAt=origin
c.box("globalBox")
l=Light()
l.hooked_on(camera.location-X)
camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray.


#################################################
#  Now, what you see
#################################################

