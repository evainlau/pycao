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
import sys
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac

from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
import povrayshoot 


class Camera(Primitive):
    """
    """
    activeCameras=True # if  False, camera.shoot does not take photo
    showImage=True # if  False compute the image but dont show it on the screeen, if anything else, does not  even compue the image 
    
    
    def __init__(self):
        self.imageHeight=800 # in pixels
        self.imageWidth=1500
        self.angle=(20./180.*math.pi)  #  use camera.zoom() to change
		#the angle without computation headache involving tangents
        self.lookAt=point(0,0,0)
        self.sky=point(0,0,1)# the upper vector in the photo
        self.directFrame=True  # By default, direct frame with Z vertical,X on the right, Y in front of us
        self.location=point(0,-4,2)  # sensible for units in meters. the positive y are in front of us. 
        self.actors=[]
        self.filmAllActors=True
        self.file="/tmp/pycaoOutput.pov" # the place to store the photo
        self.visibilityLevel=1
        self.projection="perspective"
        self.technology="povray" #  only possibility at the moment
        self.povraylights="light_source {<"+ str(self.location[0])+","+str(self.location[1])+","+str(self.location[2]+10)+ "> color White " + "}\n\n"
        self.povrayPreamble='#include "colors.inc" \n#include "metals.inc" \nbackground {Blue}\n\n'
    def move_alone(self,M):
        self.location=M*self.location
    @property
    def shoot(self):
        if self.technology=="povray" and Camera.activeCameras:
            povrayshoot.render(self)
        return self
    @property
    def show(self):
        if self.technology=="povray" and Camera.showImage:
            subprocess.call(["povray", "+P +H"+str(self.imageHeight)+ " +W"+str(self.imageWidth),self.file])
        if self.technology=="povray" and Camera.showImage==False :
            subprocess.call(["povray", "-D +H"+str(self.imageHeight)+ " +W"+str(self.imageWidth),self.file])
        return self
    def zoom(self,x):
        """
        Resize the image by a factor x. 
        """
        cameraWidth=math.tan(self.angle/2)
        self.angle=2*math.atan((cameraWidth/x))

