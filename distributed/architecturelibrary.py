
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


class Wall(Prism):
    """ Class for walls, not necessarily rectangular or vertical, but the base is a tetragon """

    @classmethod
    def from_polyline_vector(cls,polyline,verticalVector,thickness=0,name=""):
        print("starting")
        print(cls)
        self=super(Prism,cls)#.from_polyline_vector(polyline,verticalVector)
        print(self)
        if thickness>0 :
            self.thickness=thickness
        if not name:
            self.name=name
        #self.markers
        self.markers.armature=Segment(0.5*(polyline[0]+polyline[3]),0.5*(polyline[1]+polyline[2])) # aka the line on the floor in the middle of the wall
        self.markers.center=0.25*(polyline[0]+polyline[3]+polyline[1]+polyline[2])+.5*verticalVector # aka the line on the floor in the middle of the wall
        self.markers.outsideBaseLine=Segment(polyline[2],polyline[3]) # the intersection of the floor and the exterior wall. The points are the extremal points of this line
        self.markers.insideBaseLine=Segment(polyline[0],polyline[1])
        self.markers.verticalVector=verticalVector # alread accessible by self.prismDirection but more readable alias in the context of walls
        insideVector=self.markers.outsideBaseLine.vector.cross(verticalVector)
        if (self.markers.insideBaseLine[0]-self.markers.outsideBaseLine[0]).dot(insideVector) < 0:
            insideVector=-insideVector
        self.markers.insideVector=insideVector # towards the interior of the room
        self.markers_as_functions()
        print ("done Markers")

    def add_window(self,w,center=None,glued=True):
        if center is None:
            print (self.__dict__)
            center=self.center()
        w.translate(center-w.center)
        self.amputed_by(w.hole)
        if glued:
            w.glued_on(self)

        
    # @staticmethod
    # def from_x1y1x2y2_thickness_height(x1=0,y1=0,x_2=1,y_2=0,thickness=.2,height=2):
    #     normalVector=((y_2-y_1)*X+(x_1-x_2)).normalize()
    #     return Cube.from_point_list([point(x1,y1,0)-.5*thickness*normalVector,point(x2,y2,height)+.5*thickness*normalVector])
    # @staticmethod
    # def from_2points_thickness_height(p1,p2,thickness=.2,height=2):
    #     " the points are assumed to be in the plane z=0"
    #     return Wall.from_x1y1x2y2_thickness_height(p1[0],p1[1],p2[0],p2[1],thickness,height)
    # @staticmethod
    # def from_segment_thickness_height(segment,thickness=.2,height=2):
    #     " the segment is assumed to be in the plane z=0"
    #     return Wall.from2points_thickness_height(segment.p1,segment.p2,thickness,height)


    
class Room(Compound):
    """ 
    A class to build a 3d-room from a 2D plan
    """
    def __init__(self,floor=Polyline([origin-X-Y,2*Y,2*X,-2*Y,-2*X]),wallThickness=0.2,height=2,verticalVector=Z):
        """
        This constructs a room whose exterior walls are along the floor. The interior walls are computed using 
        wall thickness. The polygon for the floor is in the plane z=0, with the points listed clockwise.
        A floor and a ceiling are added. 
        Remark: if the point are listed counterclockwise, this messes the inside and outside of the room. 
        Doable in the future: compute the index of the polygon to know if it is clockwise. 
        """
        logicalWalls=[]
        outPoints=[]
        for index,segment in enumerate(floor.segments()):
            lw=Object()
            #lw.armature=segment
            lw.insideVector=segment.vector.normalized_copy().rotate(-verticalVector,math.pi/2)
            lw.insideWall=segment.copy().translate(lw.insideVector*wallThickness*.5)
            lw.outsideWall=segment.copy().translate(-lw.insideVector*wallThickness*.5)
            lw.name="wall"+str(index)
            logicalWalls.append(lw)
        for windex,logicalWall in enumerate(logicalWalls):
            previousWall=logicalWalls[windex-1]
            logicalWall.insideLeftPoint=Point.from_2_lines(logicalWall.insideWall,previousWall.insideWall)
            previousWall.insideRightPoint=logicalWall.insideLeftPoint
            logicalWall.outsideRightPoint=Point.from_2_lines(logicalWall.outsideWall,previousWall.outsideWall)
            previousWall.outsideLeftPoint=logicalWall.outsideRightPoint
            outPoints.append(logicalWall.outsideRightPoint)
        walls=[]
        for lw in logicalWalls:
            polyline=Polyline([lw.insideLeftPoint,lw.insideRightPoint,lw.outsideLeftPoint,lw.outsideRightPoint,lw.insideLeftPoint])
            walls.append(Wall(polyline,height*verticalVector,wallThickness))
        floor=Polygon(outPoints).translate(0.000000001*verticalVector) # translation so that it is above the floor
        ceiling=floor.copy().translate(height*verticalVector)
        liste=[["wall"+str(i),wall] for i,wall in enumerate(walls)]
        Compound.__init__(self,liste+[["ceiling",ceiling],["floor",floor]])
        self.walls=walls
        #Compound.__init__(self,liste)
        #Compound.__init__(self,liste+[floor])
        #Compound.__init__(self,[floor,ceiling])

class Window(Compound):
    def __init__(self,dx,dy,dz,border,holeBorder=None,texture="Yellow_Pine"):
        """dx,dy,dz are the length,depth,height respectivly, border is the size of the border of the window """ 
        frame=Cube(dx,dy,dz)
        frame.texture=texture
        self.normal=Y
        toCut=Cube(frame.point(border,-0.01,border,"aaa"),frame.point(border,-.01,border,"nnn"))
        toCut.texture=texture
        frame.amputed_by(toCut)
        if holeBorder is None:
            holeBorder=border*.5
        # The hole will be used to cut the wall behind the window.
        hole=Cube(frame.point(holeBorder,-10000,holeBorder,"aaa"),frame.point(holeBorder,-10000,holeBorder,"nnn"))
        glass=Cube(frame.point(border,dy*.5-.001,border,"aaa"),frame.point(border,dy*.5-0.01,border,"nnn"))
        glass.texture="Glass"
        Compound.__init__(self,[frame,glass])
        self.hole=hole.glued_on(self)
        self.add_box("windowBox",frame.box())

        
class RoundWindow(Compound):
    def __init__(self,radius,depth,border,texture="Yellow_Pine"):
        """ border is the size of the border of the window """ 
        frame=Cylinder(start=origin,end=origin+depth*Y,radius=radius,length=None,booleanOpen=False)
        frame.texture=texture
        self.normal=Y
        toCut=Cylinder(start=origin-Y,end=origin+depth*Y+Y,radius=radius-border,length=None,booleanOpen=False)
        toCut.texture=texture
        frame.amputed_by(toCut)
        glass=Cylinder(start=origin+(.5*depth-.01)*Y,end=origin+(.5*depth+.01)*Y,radius=radius-border,length=None,booleanOpen=False)
        glass.texture="Glass"
        Compound.__init__(self,[frame,glass])




        
"""    
* ajouter fenetres et portes,
* ajouter des textures
* ajouter le prisme et le polygone,le wall, la Room a la doc
"""
