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

camerasInScene=[]

class Camera(Primitive):
    """
    """
    activeCameras=True # if  False, camera.shoot does not take photo
    showImage=True # if  False compute the image (with povray to png) but dont show it on the screeen, if anything else, does not  even compue the image 

    
    
    def __init__(self):
        self.imageHeight=800 # in pixels
        self.imageWidth=1500
        self.angle=(20./180.*math.pi)  #  use camera.zoom() to change
		#the angle without computation headache involving tangents
        self.lookAt=point(0,0,0)
        self.sky=vector(0,0,1)# the upper vector in the photo
        self.directFrame=True  # By default, direct frame with Z vertical,X on the right, Y in front of us
        self.location=point(0,-4,2)  # sensible for units in meters. the positive y are in front of us. 
        self.actors=[]
        self.filmAllActors=True
        self.file="/tmp/pycaoOutput.pov" # the place to store the photo
        self.visibilityLevel=1
        self.projection="perspective" # could be "orthographic", useful for checking
        self.technology="povray" #  only possibility at the moment
        self.lights=[]
        self.povraylights="light_source {<"+ str(self.location[0])+","+str(self.location[1])+","+str(self.location[2]+10)+ "> color White " + "}\n\n"
        self.povrayPreamble='#include "colors.inc" \n#include "metals.inc" \n#include "textures.inc" \n#include "shapes.inc" \nbackground {Blue}\n\nglobal_settings { ambient_light rgb <1,1,1> }'
        self.quality=9 #
        self.silent=True # to display or not a lot of information when self.show is called
        self.defaultDistance=3 # The distance from the point looked at in left/right... views
        camerasInScene.append(self)
    def move_alone(self,M):
        self.location=M*self.location
    @property
    def shoot(self):
        if self.technology=="povray" and Camera.activeCameras:
            povrayshoot.render(self)
        return self
    @property
    def show_without_viewer(self):
        if self.technology=="povray":
            command="povray"
            options=""
            if Camera.showImage:
                options+="+P "
            else :
                options+="-D "
            options+="+H"+str(self.imageHeight)+ " +W"+str(self.imageWidth) +" "
            options+="+Q"+str(self.quality)+" "
            if self.silent:
                options+="-GD -GF -GR -GS -GW -GA "
                subprocess.call([command,options,self.file])
            else:
                subprocess.call([command,options,self.file])
            return self
    def pov_to_png(self):
        #same as show for string computation except always -D
        if self.technology=="povray":
            command="povray"
            options=""
            options+="-D "
            options+="+H"+str(self.imageHeight)+ " +W"+str(self.imageWidth) +" "
            options+="+Q"+str(self.quality)
            if self.silent:
                options+="-GD -GF -GR -GS -GW -GA "
            subprocess.call([command,options,self.file])
            return self
    @property
    def show(self):
        import viewer
        viewer.ViewerWindow(self)
        return self
    
    def zoom(self,x):
        """
        Resize the image by a factor x. 
        """
        cameraWidth=math.tan(self.angle/2)
        self.angle=2*math.atan((cameraWidth/x))

    def compute_frame_vectors(self):
        self.frontVector=(self.lookAt-self.location).normalized_copy()
        self.rightVector=self.frontVector.cross(self.sky)
        if  not self.rightVector == 0*X:
            self.rightVector=self.rightVector.normalized_copy()
        else:
            self.rightVector=X
            if  (self.frontVector.cross(self.frontVector) == 0*X):
                self.rightVector=Y
        self.upVector=- self.frontVector.cross(self.rightVector).normalized_copy()
        if not self.directFrame:
            self.rightVector=-self.rightVector

