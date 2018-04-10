
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


class Bearing(Compound):
    def __init__(self,iDiameter=.02,mDiameter=.022,eDiameter=.030,thickness=.01,externalColor="Blue",internalColor="Silver"):
        out=Washer(origin,origin+thickness*Z,.5*eDiameter,.5*mDiameter).colored(externalColor)
        inner=Washer(origin,origin+thickness*Z,.5*mDiameter,.5*iDiameter).colored(internalColor)
        Compound.__init__(self,[["inner",inner],["outer",out]])
        self.box=out.box
        self.axis=out.axis

    def place_on_support(self,support):
        self.screw_on(support.axis(),adjustAlong=[self.point(.5,.5,0),support.support.point(.5,.5,1)])
        return self




class DoorHandle(Compound):
    def __init__(self,depth=.08,length=.10,eDiameter=.030,color="Silver"):
        tube1=Cylinder
        out=Washer(origin,origin+thickness*Z,.5*eDiameter,.5*mDiameter).colored(externalColor)
        inner=Washer(origin,origin+thickness*Z,.5*mDiameter,.5*iDiameter).colored(internalColor)
        Compound.__init__(self,[["inner",inner],["outer",out]])
        self.box=out.box
        self.axis=out.axis

    def place_on_support(self,support):
        self.screw_on(support.axis(),adjustAlong=[self.point(.5,.5,0),support.support.point(.5,.5,1)])
        return self


class Wall(Cube):
    @staticmethod
    def from_x1y1x2y2_thickness_height(x1=0,y1=0,x_2=1,y_2=0,thickness=.1,height=2):
        return Cube.from__point_list([point(x1,y1-thickness,0),point(x2,y2+.5*thickness,2)]

class Room(Compound):

    @staticmethod
    def from_closed_curve_and_height(polyline=,height=...):
        """
        This constructs a room whose walls follow the polyline. Each line corresponds to a wall. 
        A floor and a ceiling are added. 
        """
