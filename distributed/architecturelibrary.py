
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


class Wall(Cube):
    @staticmethod
    def from_x1y1x2y2_thickness_height(x1=0,y1=0,x_2=1,y_2=0,thickness=.2,height=2):
        normalVector=((y_2-y_1)*X+(x_1-x_2)).normalize()
        return Cube.from_point_list([point(x1,y1,0)-.5*thickness*normalVector,point(x2,y2,height)+.5*thickness*normalVector])
    @staticmethod
    def from_2points_thickness_height(p1,p2,thickness=.2,height=2):
        " the points are assumed to be in the plane z=0"
        return Wall.from_x1y1x2y2_thickness_height(p1[0],p1[1],p2[0],p2[1],thickness,height)
    @staticmethod
    def from_segment_thickness_height(segment,thickness=.2,height=2):
        " the segment is assumed to be in the plane z=0"
        return Wall.from2points_thickness_height(segment.p1,segment.p2,thickness,height)


    
class Room(Compound):
    """ 
    The room is suppose to have right angle corners so that its walls are cubes. 
    """
    def __init__(polygon=Polygon(origin-X-Y,2*Y,2*X,-2*Y,-2*X),thickness=0.2,height=2):
        """
        This constructs a room whose walls follow the polyline. Each line corresponds to a wall. 
        A floor and a ceiling are added. 
        """
        listOfWalls=[]
        for s in polyline.segments():
            listOfWalls.append(Wall.from_segment_thickness_height(s.prolonged_on_left(0.5*thickness).prolonged_on_right(0.5*thickness)))
        Compound.__init__(self,[["walls",listOfWalls],["ceiling",polygon.translate(height*Z)],["floor",polygon]])

    @staticmethod
    def from_polyline_thickness_height(polygon=Polygon(origin-X-Y,2*Y,2*X,-2*Y,-2*X),thickness=.2,height=2):
        return Room(polygon,thickness,height)


* a faire : classe polygone, qui herite de polyline et son rendu dans povray shoot.
* tester
* ajouter fenetres et portes,
* ajouter des textures
* Eventuellement faire avec des murs fins.
