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
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core/"
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


camera.zoom(0.655)
camera.imageHeight=800 # in pixels
camera.imageWidth=1200 
camera.quality=11 # a number between 0 and 11,  Consider using a lower quality setting if you're just testing your scene


camera.lookAt=origin#+3*X+.75*Z # look at the center of cyl

#camera.actors=[] # If you want to fill this list and use it, you should set camera.filmAllActors to False. 
camera.filmAllActors=True # overrides the camera.actors list



camera.hooked_on(origin+1.6*X-4*Y+3.6*Z)  # the positive y are in front of us if the camera is located in negative Y and we look at  a point close to the origin
light=Light().hooked_on(origin+8*X+10*Z) # a light located close to the camera
light=Light().hooked_on(origin+8*X+.2*Y+10*Z) # a light located close to the camera
light=Light().hooked_on(origin+8*X-.3*Y+10*Z) # a light located close to the camera

#######################################

"""
                SCENE DESCRIPTION
"""


directory=os.path.dirname(os.path.realpath(__file__))
base=os.path.basename(__file__)
camera.file=directory+"/generatedImages/"+os.path.splitext(base)[0]+"1.pov"
camera.povraypath=pycaoDir+"/../images/" # where you put your images,photos for the textures
#bbloc1
p=plane(Z,origin)
pig1=Pigment("Coral") # a color known by povray
pig2=Pigment.from_photo("oak.png",dimx=3.,dimy=10.,symmetric=True) # a pigment constructed by Pycao
normal1=Normal("bozo 1.5 scale .04") # A normal which is a valid povray string
finish1=Finish(" ambient .35 diffuse .1 phong .023 phong_size 15")
t1=Texture(pig1,normal1,finish1) # We put the elements in a texture
t2=Texture(pig2,finish1)
p.textured(t2) # we apply on our object
s=Sphere(origin+.35*Z,.5).textured(t1).scale(1.05,1.03,1)
#ebloc1
camera.shoot
camera.pov_to_png
camera.file=directory+"/generatedImages/"+os.path.splitext(base)[0]+"2.pov"
#bbloc2
finish2=Finish(" phong .023 phong_size 15")
finish2.enhance(" ambient .2 diffuse .08 ") #PNF items enhanced by string
t=Sphere(origin+.35*Z-1*X,.5).colored("Yellow").scale(1.9,1.03,1)
t.texture.enhance(normal1).enhance(finish2) #Texture enhanced by a PNFT item 
normal2=Normal("bumps .55 scale .061") # A normal which is a valid povray string
p.add_to_texture(normal2) # enhancing the object directly rather than the texture. 
#ebloc2
camera.shoot
camera.pov_to_png
    


#################################################
#  Now, what you see
#################################################


