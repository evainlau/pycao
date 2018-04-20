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


from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
import povrayshoot 
from cameras import *


        
class Light(ObjectInWorld):
    """
    """
    def __init__(self,location=origin,color="rgb <2,2,2>"):
        self.location=location
        self.add_handle("location",location)
        self.color=color
    def move_alone(self,M):
        self.location=M*self.location
        return self



class PhysicalLamp(Compound):
    """" returns an object with 2 handles, one for the light, one for hanging on the wall/ceiling """
    def __init__(self):
            #physicalLamp=Cube(origin,origin+.4*X+.4*Y+.4*Z)
            cone=Cone(origin-.05*Z,origin+.2*Z,.4,.20,booleanOpen=True)
            cone.texture="pigment {rgb<.55,.5,.5> filter .2} finish{diffuse .5 brilliance 0  ambient .3}"
            cone.name="Lampe"
            cylinder1=Cylinder(origin+.2*Z,origin+.3*Z,0.005).colored("Black")
            cylinder2=Cylinder(origin+.3*Z,origin+.32*Z,.05).colored("Black")
            self.add_list_to_compound([cone,cylinder2,cylinder1])
            self.add_handle("ceiling",origin+.32*Z)
            self.add_handle("light",origin)
            
class Lamp(Compound):
    """ a union of a light and a physicallamp, the handle of the physicalLamp is transmitted to the Lamp.""" 
    def __init__(self,physicalLamp=None,light=None,cameraList=None):
        if cameraList is None:
            cameraList=camerasInScene
            print("cameraList",cameraList)
        if physicalLamp is None:
            physicalLamp=PhysicalLamp()
        if light is None:
            light=Light(origin) # a light
            light.color="White"
        #print("lampPyhand", physicalLamp.print_handles())
        physicalLamp.select_handle("light") # since the lamp has an other handle to the ceiling
        print("handles de la light")
        light.handle()
        light.print_handles()
        light.hooked_on(physicalLamp) 
        for camera in cameraList:
            #print("avant",camera.lights)
            camera.lights.append(light)
            #print("apres",camera.lights)
        self.add_list_to_compound([["light",light],["object",physicalLamp]])
        self.add_handle("ceiling",physicalLamp.select_handle("ceiling"))
        
