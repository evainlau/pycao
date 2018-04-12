
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
    def __init__(floor=Polygon(origin-X-Y,2*Y,2*X,-2*Y,-2*X),wallThickness=0.2,height=2):
        """
        This constructs a room whose exterior walls are along the floor. The interior walls are computed using 
        wall thickness. The polygon for the floor is in the plane z=0, with the points listed clockwise.
        A floor and a ceiling are added. 
        Remark: if the point are listed counterclockwise, this messes the inside and outside of the room. 
        Doable in the future: compute the index of the polygon to know if it is clockwise. 
        """
        walls=[]
        for segment,segment.index in polyline.segments():
            wall=Object()
            wall.armature=segment
            wall.insideVector=segment.normalized_copy().rotate(-Z,math.pi/2)
            wall.insideWall=segment.copy().translate(wall.insideVector*wallThickness*.5)
            wall.outsideWall=segment.copy().translate(-wall.insideVector*wallThickness*.5)
            wall.height=height
            wall.name="wall"+str(segment.index)
            walls.append(wall)
        intPoints=[]
        extPoints=[]
        for wall,wall.index in walls:
            previousWall=walls[wall.index-1]
            wall.insideLeftPoint=point.from_2_lines(wall.insideWall,previousWall.insideWall)
            previousWall.insideRightPoint=wall.insideLeftPoint
            intPoints.append(wall.insideLeftPoint)
            wall.outsideLeftPoint=point.from_2_lines(wall.outsideWall,previousWall.outsideWall)
            previousWall.outsideRightPoint=wall.outsideLeftPoint
            intPoints.append(wall.outsideLeftPoint)
            walls.append(Wall(wall))
        floor=polygon(intPoints)
        ceiling=floor.copy.translate(height*Z)
        Compound.__init__(self,[["walls",walls],["ceiling",ceiling],["floor",floor]])



"""    
* faire des wall qui heritent de prisme
* ajouter fenetres et portes,
* ajouter des textures
* Eventuellement faire avec des murs fins.
* ajouter le prisme et le polygone a la doc
"""
