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
   w=Cube(3,3,3).colored('Brown')
   seg=w.boxline(None,0.5,0.5,"pp") # a line where y=.5,z=.5 are fixed in the middle of the cube and  x=None varies
   cyl=ICylinder(seg,0.2).colored('SpicyPink')
   seg2=w.boxline(0.5,None,0.5,"pp")
   cyl2=ICylinder(seg2,0.2).colored('Yellow')
   seg3=w.boxline(0.5,0.5,None,"pp")
   cyl3=ICylinder(seg3,0.2).colored('Violet')
   p=w.boxplane(Z,-2.5,"p").colored("Orange")

   camera.zoom(.15)
   camera.povraylights="light_source {<-2,0,6.8> color White " + "}\n\n"
   camera.lookAt=w.center
   camera.actors=[w,cyl,cyl2,cyl3,p]





#################################################
#  Now, what you see
#################################################

#camera.file="docPictures/footprintsLinesAndPlane.pov" # A name for the povray file that will be generated. Must end with .pov
directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
print(camera.file)
camera.povraypath=pycaoDir+"images/" # where you put your images,photos for the textures
camera.zoom(1.5)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=9 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene




#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.location=origin-X-3.3*Y+5.*Z
light=Light().hooked_on(camera.hook()+1*X+1*Z) # a light located close to the camera

camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
camera.pov_to_png # show the photo, ie calls povray. 
