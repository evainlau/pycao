
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
    """ Class for walls, not necessarily rectangular or vertical, but the base is a tetragon 
    Points numbers 0,1 are by definition on the interior of the wall (numbers 2,3 are on the outside wall """

    @classmethod
    def from_polyline_vector(cls,polyline,verticalVector,thickness=0,name=""):
        self=super(Wall,cls).from_polyline_vector(polyline,verticalVector)
        if thickness>0 :
            self.thickness=thickness
        if name:
            self.name=name
        #self.markers
        if not hasattr(self,"markers"):
            self.markers=Object()
        self.markers.armature=Segment(0.5*(polyline[0]+polyline[3]),0.5*(polyline[1]+polyline[2])) # aka the line on the floor in the middle of the wall
        self.markers.center=0.25*(polyline[0]+polyline[3]+polyline[1]+polyline[2])+.5*verticalVector # aka the line on the floor in the middle of the wall
        self.markers.outsideBaseLine=Segment(polyline[2],polyline[3]) # the intersection of the floor and the exterior wall. The points are the extremal points of this line
        self.markers.insideBaseLine=Segment(polyline[0],polyline[1])
        self.markers.verticalVector=verticalVector.copy() # alread accessible by self.prismDirection but more readable alias in the context of walls
        insideVector=self.markers.outsideBaseLine.vector.cross(verticalVector).normalize()
        if (self.markers.insideBaseLine.p1-self.markers.outsideBaseLine.p2).dot(insideVector) < 0:
            insideVector=-insideVector
        self.markers.insideVector=insideVector # towards the interior of the room
        correctiveMap=self.mapFromParts.inverse()
        markersList=[ a for a in dir(self.markers) if not a.startswith('__')]
        for markerName in markersList: #self.map_fromParts is not identity in the prism, thus the marker should be corrected to compensate
            marker=getattr(self.markers,markerName)
            marker.move(correctiveMap)
        self.markers_as_functions()
        return self

    def add_apperture(self,w,center=None): # type = winoow or doord
        mape=Map.rotational_difference(w.normal,self.insideVector())
        w.move(mape)
        if center is None:
            center=self.center()
        w.translate(center-w.center)
        self.amputed_by(w.hole)

        
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
    def __init__(self,floor=Polyline([origin-X-Y,2*Y,2*X,-2*Y,-2*X]),insideThickness=.25,outsideThickness=0,height=2.5,verticalVector=Z,texture="pigment{ color rgb <0.75,0.5,0.3>}  "):
        """
        This constructs a room whose exterior walls are along the floor. The interior walls are computed using 
        wall thickness. The polygon for the floor is in the plane z=0, with the points listed clockwise.
        A floor and a ceiling are added. 
        Remark: if the point are listed counterclockwise, this messes the inside and outside of the room. 
        Doable in the future: compute the index of the polygon to know if it is clockwise. 
        """
        logicalWalls=[]
        outPoints=[]
        self.windows=[]
        self.doors=[]
        self.height=height
        for index,segment in enumerate(floor.segments()):
            lw=Object()
            #lw.armature=segment
            lw.insideVector=segment.vector.normalized_copy().rotate(-verticalVector,math.pi/2)
            lw.insideWall=segment.copy().translate(lw.insideVector*insideThickness)
            lw.outsideWall=segment.copy().translate(-lw.insideVector*outsideThickness)
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
            theWall=Wall.from_polyline_vector(polyline,height*verticalVector,insideThickness+outsideThickness)
            theWall.texture=texture
            walls.append(theWall)
        floor=Polygon(outPoints).translate(0.000000001*verticalVector).colored("OldGold") # translation so that it is above the floor
        ceiling=floor.copy().translate(height*verticalVector).colored("White")
        liste=[["wall"+str(i),wall] for i,wall in enumerate(walls)]
        Compound.__init__(self,liste+[["ceiling",ceiling],["floor",floor]])
        self.walls=walls

    def add_window(self,wallNumber,wlength,wheight,wdepth,deltaLength,deltaHeigth,fromOutside=True,glued=True):
        """ adds a window of size (wlength,wheight,wdepth) on wall wallNumber, located 
        at deltaLength meters from the right of the outside wall ( or optionnally from the left of the inside wall), 
        and deltaHeigth meters above the floor """
        wthickness=.1
        w=Window(wlength,wdepth,wheight,wthickness)
        wall=self.walls[wallNumber]
        if fromOutside:
            windowCenter=wall.outsideBaseLine().point(deltaLength+0.5*wlength,"n")+(deltaHeigth+.5*wheight)*wall.verticalVector().normalized_copy()+wall.insideVector().normalize()*wall.thickness
        else:
            windowCenter=wall.insideBaseLine().point(deltaLength+0.5*wlength,"a")+(deltaHeigth+.5*wheight)*wall.verticalVector().normalized_copy()
        wall.add_apperture(w,windowCenter)
        self.windows.append(w)
        if glued:
            w.glued_on(self)


    def add_door(self,wallNumber,wlength,wheight,wdepth,deltaLength,deltaHeigth=0,fromOutside=True,reverseHandle=False,glued=True):
        """ adds a window of size (wlength,wheight,wdepth) on wall wallNumber, located 
        at deltaLength meters from the right of the outside wall ( or optionnally from the left of the inside wall), 
        and deltaHeigth meters above the floor """
        dthickness=.1
        w=Door(wlength,wdepth,wheight,reverseHandle)
        wall=self.walls[wallNumber]
        if fromOutside:
            doorCenter=wall.outsideBaseLine().point(deltaLength+0.5*wlength,"n")+(deltaHeigth+.5*wheight)*wall.verticalVector().normalized_copy()+wall.insideVector().normalize()*wall.thickness
        else:
            doorCenter=wall.insideBaseLine().point(deltaLength+0.5*wlength,"a")+(deltaHeigth+.5*wheight)*wall.verticalVector().normalized_copy()
        wall.add_apperture(w,doorCenter)
        self.doors.append(w)
        if glued:
            w.glued_on(self)
        return w

    def add_perpendicular_wall(self,wallNumber,distance,wallLength,thickness,measurementType="a",offset=0,height=None):
        """ add a wall perpendicular to an outside wall. Measure from left by default and from the right if measurment type == "n" 
         By default, the height of the wall is taken from the room height. 
        If an offset is given, a space is added between the 2 walls"""
        if height is None:
            height=self.height
        myWall=self.walls[wallNumber]
        delta=.5*thickness
        vec=myWall.insideVector().normalize()
        basePointInside=myWall.insideBaseLine().point(distance-delta,measurementType)+offset*vec
        basePointOutside=myWall.insideBaseLine().point(distance+delta,measurementType)+offset*vec
        endPointInside=basePointInside+wallLength*vec
        endPointOutside=basePointOutside+wallLength*vec
        #print([basePointInside,endPointInside,basePointOutside,endPointOutside,basePointInside])
        wall=Wall.from_polyline_vector(Polyline([basePointInside,endPointInside,endPointOutside,basePointOutside,basePointInside]),self.height*Z,thickness=thickness)
        self.add_to_compound(wall)
        self.walls.append(wall)
        return wall

    
        
class Window2(Compound):
    def __init__(self,dx,dy,dz,border,holeBorder=None,texture="Yellow_Pine"):
        """dx,dy,dz are the length,depth,height respectivly, border is the size of the border of the window """ 
        frame=Cube(dx,dy,dz)
        frame.texture=texture
        toCut=Cube(frame.point(border,-0.01,border,"aaa"),frame.point(border,-.01,border,"nnn"))
        toCut.texture=texture
        frame.amputed_by(toCut)
        if holeBorder is None:
            holeBorder=border*.5
        # The hole will be used to cut the wall behind the window.
        hole=Cube(frame.point(holeBorder,-10000,holeBorder,"aaa"),frame.point(holeBorder,-10000,holeBorder,"nnn"))
        glass=Cube(frame.point(border,dy*.5-.001,border,"aaa"),frame.point(border,dy*.5-0.01,border,"nnn"))
        glass.texture="Glass"
        Compound.__init__(self,[frame,glass,["normal",Y.copy()]])
        self.hole=hole.glued_on(self)
        self.hole.visibility=0
        self.add_box("windowBox",frame.box())

        
class Window(Compound):
    def __init__(self,dx,dy,dz,border,holeBorder=None,texture="Cork pigment{White}"):#"Yellow_Pine"):
        """dx,dy,dz are the length,depth,height respectivly, border is the size of the border of the window """ 
        frame=RoundBox.from_dimensions(dx,dy,dz,.03)
        frame2=Cube(dx,dy,dz)
        frame.texture=texture
        toCut=Cube(frame2.point(border,-0.01,border,"aaa"),frame2.point(border,-.01,border,"nnn"))
        toCut.texture=texture
        frame.amputed_by(toCut)
        if holeBorder is None:
            holeBorder=border*.5
        # The hole will be used to cut the wall behind the window.
        hole=Cube(frame2.point(holeBorder,-10000,holeBorder,"aaa"),frame2.point(holeBorder,-10000,holeBorder,"nnn"))
        glass=Cube(frame2.point(border,dy*.5-.001,border,"aaa"),frame2.point(border,dy*.5-0.01,border,"nnn"))
        glass.texture="Glass"
        Compound.__init__(self,[frame,glass,["normal",Y.copy()]])
        self.hole=hole.glued_on(self)
        self.hole.visibility=0
        self.add_box("windowBox",frame2.box())

class Door(Compound):
    def __init__(self,dx=.9,dy=.03,dz=2.15,reverseHandle=False,holeBorder=0.1,doorhandle=None):
        """dx,dy,dz are the length,depth,height respectivly, the holeBorder is difference between the door and the hole
        The option reverseHandle is set to change the handle position from left to Right """
        
        frame=Cube(dx,dy,dz)
        #toCut=Cube(frame.point(border,-0.01,border,"aaa"),frame.point(border,-.01,border,"nnn"))
        #toCut.texture=texture
        #frame.amputed_by(toCut)
        #if holeBorder is None:
        #    holeBorder=border*.5
        # The hole will be used to cut the wall behind the window.
        if doorhandle is None:
            doorhandle=DoorHandle()
        doorhandle.glued_on(self)
        doorhandle2=doorhandle.copy().move(Map.linear(-X,Y,Z)).glued_on(self)
        hole=Cube(frame.point(holeBorder,-10000,holeBorder,"aaa"),frame.point(holeBorder,-10000,holeBorder,"nnn"))
        #glass=Cube(frame.point(border,dy*.5-.001,border,"aaa"),frame.point(border,dy*.5-0.01,border,"nnn"))
        #glass.texture="Glass"
        if not reverseHandle:
            handlePointToLock1=frame.point(.1,0,1.05,"apa")
            handlePointToLock2=frame.point(.1,1,1.05,"apa")
            doorhandle2.self_rotate(math.pi)
        else:
            handlePointToLock2=frame.point(.1,0,1.05,"npa")
            handlePointToLock1=frame.point(.1,1,1.05,"npa")
            doorhandle.self_rotate(math.pi)
        doorhandle.translate(handlePointToLock1-doorhandle.handlePoint)
        doorhandle2.translate(handlePointToLock2-doorhandle2.handlePoint)
        Compound.__init__(self,[frame,["normal",Y.copy()]])
        self.hole=hole.glued_on(self)
        self.hole.visibility=0
        self.add_box("windowBox",frame.box())

        
    def add_porthole(self,texture="Cork pigment{White}"): # type = winoow or doord
        w=RoundWindow(radius=.2,depth=.15,border=.02,texture=texture)
        #print(self.box().segment(None,.5,.5,"ppp"))
        mape=Map.rotational_difference(w.normal,self.box().segment(.5,None,1.6,"ppa").vector)
        w.move(mape)
        w.translate(self.point(.5,.5,1.6,"ppa")-w.frame.axis().point(.5,"p"))
        self.amputed_by(w.hole)
        w.glued_on(self)
        return self
        
        
class RoundWindow(Compound):
    def __init__(self,radius,depth,border,texture="Yellow_Pine"):
        """ border is the size of the border of the window """ 
        frame=Cylinder(start=origin,end=origin+depth*Y,radius=radius,length=None,booleanOpen=False)
        frame.texture=texture
        self.normal=Y.copy()
        toCut=Cylinder(start=origin-Y,end=origin+depth*Y+Y,radius=radius-border,length=None,booleanOpen=False)
        toCut.texture=texture
        frame.amputed_by(toCut)
        glass=Cylinder(start=origin+(.5*depth-.01)*Y,end=origin+(.5*depth+.01)*Y,radius=radius-border,length=None,booleanOpen=False)
        glass.texture="Glass"
        self.hole=toCut.glued_on(self)
        self.hole.visibility=0
        Compound.__init__(self,[["frame",frame],glass])

class Table(Compound):
    def __init__(self,length,width,heigth,thickness,thickness2=.1,wireRadius=.03):
        top=RoundBox.from_dimensions(length,width,thickness,wireRadius)
        basee=Cube(length-.05,width-.05,thickness2)
        top.above(basee)
        legLenth=heigth-thickness-thickness2
        Compound.__init__(self,[["top",top],basee])
        for string in ["aaa","ana","naa","nna"]:
            pointe=basee.point(.05,.05,0,string)
            leg=Cylinder(pointe,pointe-legLenth*Z,.03)
            self.add_to_compound(leg)
        self.translate(legLenth*Z)
        #the point on the floor below the center of the table
        centerOnFloor=top.point(0.5,.5,.5,"ppp")
        centerOnFloor[2]=0
        self.add_to_compound(["centerOnFloor",centerOnFloor])
        self.add_box("tableBox",Cube([origin,point(length,width,heigth)]).box())

class Chair(Compound):
    def __init__(self):
        legLenth=.45
        seat=RoundBox.from_dimensions(.30,.35,.04,.015)
        p1=point(.05,.35,.4)
        p3=point(.30,.35,.4)
        p2=point(.175,.4,.4)
        t=Torus.from_3_points(p1,p2,p3,.02)
        s1=Sphere(p1,.02)
        s2=Sphere(p3,.02)
        start=t.circle(.4)#0.110978533178,0.388316548251
        start2=point(.3-.110978,.388316,.4)
        end2=seat.point(.12,.06,.5,"nnp")
        end=seat.point(.12,.06,.5,"anp")
        c=Cylinder(start,end,radius=.015)
        c2=Cylinder(start2,end2,radius=.015)
        Compound.__init__(self,[t,s1,s2,c,c2,seat])
        for string in ["aaa","ana","naa","nna"]:
            pointe=seat.point(.05,.05,0,string)
            leg=Cylinder(pointe,pointe-legLenth*Z,.02)
            self.add_to_compound(leg)
        self.center_on_floor=seat.point(.5,.5,.5,"ppp")
        self.center_on_floor[2]=0
        axis=seat.segment(.5,.5,None,"ppp")
        self.add_axis("axeVertical",axis)
        self.add_box("",seat.box())

class Stove(Compound):
    def __init__(self,roomHeight=2.5,texture="Cork pigment{Black}"):
        door=Window(.4,.05,.6,.05,holeBorder=None,texture=texture)
        fireplace=RoundBox.from_dimensions(.4,.4,.6,.01)
        spacer=Cube(.38,.01,.58)
        spacer2=Cube(.38,.38,.01)        
        spacer.behind(door)
        fireplace.behind(spacer)
        spacer2.below(fireplace)
        floorPoint=spacer2.point(.5,.5,0,"ppp")
        cylstart=fireplace.point(.5,.5,1,"ppp")
        cylEnd=cylstart+(roomHeight-.61)*Z
        cyl=Cylinder(cylstart,cylEnd,.08)
        self.add_list_to_compound([door,spacer,fireplace,spacer2,cyl,["floorPoint",floorPoint]])
        self.add_axis("axis",fireplace.segment(.5,.5,None,"ppp"))

class DoorHandle(Compound):
    def __init__(self,texture="New_Brass",left=True):
        bottom=Cylinder(origin,origin+.005*Y,radius=.025)
        middle=Cube.from_list_of_points([origin-.025*X+.0*Z,origin+.025*X+.05*Z+.005*Y])
        top=copy.deepcopy(bottom)
        top.translate(.05*Z)
        start=middle.point(.5,-1,.75,"ppp")
        axis=Cylinder.from_point_vector(start,-.03*Y,.01)
        verticalAxis=middle.segment(.5,.5,None,"ppp")
        start=start-.02*Y
        handle=Torus.from_3_points(start,start+.03*X,start+.07*X-.02*Z,.01)
        handlePoint=middle.point(.5,1,.75,"ppp")
        self.add_list_to_compound([bottom,["middle",middle],top,axis,handle,["handlePoint",handlePoint]])
        self.texture=texture
        scaleFactor=2
        mape=Map.linear(scaleFactor*X,scaleFactor*Y,scaleFactor*Z)
        self.move(mape)
        if not left: # this handle goes to the right of the door
            self.move(Map.linear(-X,Y,Z))
        self.add_axis("verticalAxis",verticalAxis)

class Lamp(Compound):
    def __init__(self,location,physicalLamp=None,light=None,lightColor="White",cameraList=None):
        if cameraList is None:
            cameraList=camerasInScene
        if physicalLamp is None:
            physicalLamp=Sphere(origin,.1)
            physicalLamp.texture="pigment {White filter 1}"
        if light is None:
            light=Light(origin) # a light
            lightColor=lightColor
        for camera in cameraList:
            camera.lights.append(light)
        self.add_list_to_compound([["light",light],["object",physicalLamp]])
        self.add_box("defaultBox",physicalLamp.box())
        print("yes",physicalLamp.box())
        print(self)
        self.move_at(location)
        
""" 
* ameliorer la lampe pour ajouter un fil qui pendouille, puis un handle pour la mettre au plafond
* faire une liste de handles et une methode join_handlePoints. 
* ajouter le thick triangle
* debugger le plan qui n'est pas bouge' proprement par une action non orthogonale
* ajouter des objets : 2 armoires, \'etagere, carrelage, lampe, amelioration fenetres
bouger la chair avec un above comme la table. 
* implementer les textures
* ajouter le prisme et le polygone,le wall, la Room,fenetres a la doc, la librairie archi, la rounded box, 
le torus
dire que above marche avec des points dans la doc. 
"""