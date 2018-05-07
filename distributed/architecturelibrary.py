from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
from material import *
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
        return self
        
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
    def __init__(self,floor=Polyline([origin-X-Y,2*Y,2*X,-2*Y,-2*X]),insideThickness=.25,outsideThickness=0,height=2.5,verticalVector=Z, rgb=[0.75,0.5,0.3]):
        """
        This constructs a room whose exterior walls are along the floor. The interior walls are computed using 
        wall thickness. The polygon for the floor is in the plane z=0, with the points listed clockwise.
        A floor and a ceiling are added. 
        Remark: if the point are listed counterclockwise, this messes the inside and outside of the room. 
        Doable in the future: compute the index of the polygon to know if it is clockwise. 
        """
        self.name="Room"
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
            theWall.rgbed(rgb)
            walls.append(theWall)
        floor=Polygon(outPoints).translate(0.000000001*verticalVector).colored("OldGold") # translation so that it is above the outside floor
        ceiling=floor.copy().translate(height*verticalVector).colored("White")
        floor.name="Ceiling"
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
        return w

    def add_door(self,wallNumber,wlength,wheight,wdepth,deltaLength,deltaHeigth=0,fromOutside=True,reverseHandle=False,glued=True,handleTexture=Texture("New_Brass")):
        """ adds a window of size (wlength,wheight,wdepth) on wall wallNumber, located 
        at deltaLength meters from the right of the outside wall ( or optionnally from the left of the inside wall), 
        and deltaHeigth meters above the floor """
        dthickness=.1
        w=Door(wlength,wdepth,wheight,reverseHandle,handleTexture=handleTexture)
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
    def __init__(self,dx,dy,dz,border,holeBorder=None,color="Yellow_Pine"):
        """dx,dy,dz are the length,depth,height respectivly, border is the size of the border of the window """ 
        frame=Cube(dx,dy,dz)
        frame.colored(color)
        toCut=Cube(frame.point(border,-0.01,border,"aaa"),frame.point(border,-.01,border,"nnn"))
        toCut.colored(color)
        frame.amputed_by(toCut)
        if holeBorder is None:
            holeBorder=border*.5
        # The hole will be used to cut the wall behind the window.
        hole=Cube(frame.point(holeBorder,-10000,holeBorder,"aaa"),frame.point(holeBorder,-10000,holeBorder,"nnn"))
        glass=Cube(frame.point(border,dy*.5-.001,border,"aaa"),frame.point(border,dy*.5-0.01,border,"nnn"))
        glass.new_texture(Texture("Glass"))
        Compound.__init__(self,[frame,glass,["normal",Y.copy()]])
        self.hole=hole.glued_on(self)
        self.hole.visibility=0
        self.add_box("windowBox",frame.box())

        
class Window(Compound):
    def __init__(self,dx,dy,dz,border,holeBorder=None,texture=Texture("Cork")):#"Yellow_Pine"):
        """dx,dy,dz are the length,depth,height respectivly, border is the size of the border of the window """ 
        frame=RoundBox.from_dimensions(dx,dy,dz,.03)
        frame2=Cube(dx,dy,dz)
        frame.new_texture(texture)
        toCut=Cube(frame2.point(border,-0.01,border,"aaa"),frame2.point(border,-.01,border,"nnn"))
        toCut.new_texture(texture)
        frame.amputed_by(toCut)
        if holeBorder is None:
            holeBorder=border*.5
        # The hole will be used to cut the wall behind the window.
        hole=Cube(frame2.point(holeBorder,-10000,holeBorder,"aaa"),frame2.point(holeBorder,-10000,holeBorder,"nnn"))
        glass=Cube(frame2.point(border,dy*.5-.001,border,"aaa"),frame2.point(border,dy*.5-0.01,border,"nnn"))
        glass.name="Window Glass"
        glass.new_texture(Texture("Glass"))
        Compound.__init__(self,[["frame",frame],["glass",glass],["normal",Y.copy()]])
        self.hole=hole.glued_on(self)
        self.hole.visibility=0
        self.add_box("windowBox",frame2.box())

class Door(Compound):
    def __init__(self,dx=.9,dy=.03,dz=2.15,reverseHandle=False,holeBorder=0.1,doorhandle=None,handleTexture=None):
        """dx,dy,dz are the length,depth,height respectivly, the holeBorder is difference between the door and the hole
        The option reverseHandle is set to change the handle position from left to Right """
        
        frame=RoundBox.from_dimensions(dx,dy,dz,.025)
        #toCut=Cube(frame.point(border,-0.01,border,"aaa"),frame.point(border,-.01,border,"nnn"))
        #toCut.texture=texture
        #frame.amputed_by(toCut)
        #if holeBorder is None:
        #    holeBorder=border*.5
        # The hole will be used to cut the wall behind the window.
        if doorhandle is None:
            doorhandle=DoorHandle(handleTexture)
        doorhandle.glued_on(self)
        self.dhandle1=doorhandle
        doorhandle2=doorhandle.copy().move(Map.linear(-X,Y,Z)).glued_on(self)
        self.dhandle2=doorhandle2
        hole=Cube(frame.point(holeBorder,-10000,holeBorder,"aaa"),frame.point(holeBorder,-10000,holeBorder,"nnn"))
        #glass=Cube(frame.point(border,dy*.5-.001,border,"aaa"),frame.point(border,dy*.5-0.01,border,"nnn"))
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

        
    def add_porthole(self,texture=Texture("Cork")): # type = winoow or doord
        w=RoundWindow(radius=.2,depth=.15,border=.02,texture=texture)
        #print(self.box().segment(None,.5,.5,"ppp"))
        mape=Map.rotational_difference(w.normal,self.box().segment(.5,None,1.6,"ppa").vector)
        w.move(mape)
        w.translate(self.point(.5,.5,1.6,"ppa")-w.frame.axis().point(.5,"p"))
        self.amputed_by(w.hole)
        w.glued_on(self)
        self.window=w
        return w
        
        
class RoundWindow(Compound):
    def __init__(self,radius,depth,border,texture=Texture("Yellow_Pine")):
        """ border is the size of the border of the window """ 
        frame=Cylinder(start=origin,end=origin+depth*Y,radius=radius,length=None,booleanOpen=False)
        frame.new_texture(texture)
        self.normal=Y.copy()
        toCut=Cylinder(start=origin-Y,end=origin+depth*Y+Y,radius=radius-border,length=None,booleanOpen=False)
        toCut.new_texture(texture)
        frame.amputed_by(toCut)
        glass=Cylinder(start=origin+(.5*depth-.01)*Y,end=origin+(.5*depth+.01)*Y,radius=radius-border,length=None,booleanOpen=False)
        glass.new_texture(Texture("Glass"))
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
    def __init__(self,roomHeight=2.5,texture=Texture("New_Brass")):
        door=Window(.4,.05,.6,.05,holeBorder=None,texture=texture)
        fireplace=RoundBox.from_dimensions(.4,.4,.6,.01).new_texture(texture)
        spacer=Cube(.38,.01,.58).new_texture(texture)
        spacer2=Cube(.38,.38,.01).new_texture(texture)
        spacer.behind(door)
        fireplace.behind(spacer)
        spacer2.below(fireplace)
        floorPoint=spacer2.point(.5,.5,0,"ppp")
        cylstart=fireplace.point(.5,.5,1,"ppp")
        cylEnd=cylstart+(roomHeight-.61)*Z
        cyl=Cylinder(cylstart,cylEnd,.08).new_texture(texture)
        self.add_list_to_compound([["door",door],["spacer",spacer],fireplace,spacer2,cyl,["floorPoint",floorPoint]])
        self.add_axis("axis",fireplace.segment(.5,.5,None,"ppp"))

class DoorHandle(Compound):
    def __init__(self,texture=Texture("New_Brass "),left=True):
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
        self.new_texture(texture)
        scaleFactor=2
        mape=Map.linear(scaleFactor*X,scaleFactor*Y,scaleFactor*Z)
        self.move(mape)
        if not left: # this handle goes to the right of the door
            self.move(Map.linear(-X,Y,Z))
        self.add_axis("verticalAxis",verticalAxis)

class Glass(Compound):
    def __init__(self,start=origin,end=origin+.2*Z,radius=.05):
        base=Cylinder(start,end,radius)
        toCut=Cylinder(start+.02*Z,end+.05*Z,radius-.001)
        base.amputed_by(toCut)
        self.add_hook("bottom",origin)
        self.add_to_compound(base)
        self.new_texture("Glass")
        self.add_to_texture("pigment {color rgbt <1,1,1,.58>}")

class LightSwitch(Compound):
    def __init__(self,size=.12):
        support=Cube(origin+.003*Y,origin+size*X+size*Z+.0035*Y)
        base=RoundBox(origin,origin+size*X+size*Z+.003*Y,.001,False)
        toCut=Cube(origin+.02*X+.02*Z-Y,origin+(size-.02)*X+(size-.02)*Z+Y)
        button=Cube(origin+.023*X+.023*Z-.003*Y,origin+(size-.023)*X+(size-.023)*Z+.003*Y).translate(-.003*Y)
        p1=button.point(0,0,0,"ppp")
        p2=button.point(0,1,1,"ppp")
        p3=button.point(1,1,1,"ppp")
        P=plane.from_3_points(p1,p2,p3)
        button.amputed_by(P)
        base.amputed_by(toCut)
        self.add_list_to_compound([base,button,support])
        self.new_texture("pigment {White}")
        support.new_texture("pigment {Grey}")
        self.add_box("default",base.box())
        self.add_axis("outsideVector",self.box().segment(.5,None,.5,"ppp"))
        self.add_hook("to_wall",self.box().point(.5,1,.5,"ppp"))


        
class Tiling(Compound):
    def __init__(self,tile,jointWidth,jointHeight,xnumber,ynumber,polyline=None):
        """
        The tile has a box from which the dimensions are read. 
        """
        p=tile.point(0,0,0,"ppp")
        q=tile.point(1,1,1,"ppp")
        r=tile.point(0,0,1,"ppp")
        xdim=(q-p)[0]
        ydim=(q-p)[1]
        zdim=(q-p)[2]
        for i in range(xnumber):
            for j in range(ynumber):
                ntile=tile.copy()
                ntile.translate(origin-p+i*(xdim+jointWidth)*X+j*(ydim+jointWidth)*Y)
                tcop=ntile.copy()
                self.add_to_compound(tcop)
        if jointHeight >0:
            mortar=Cube(origin,origin+xnumber*(xdim+jointWidth)*X+ynumber*(ydim+jointWidth)*Y+jointHeight*Z).colored("Black")
            self.add_to_compound(mortar)
        fb=Cube(origin,origin+xnumber*(xdim+jointWidth)*X+ynumber*(ydim+jointWidth)*Y+(r-p)).box()
        self.add_box("globalBox",fb)
        self.add_hook("bottomInitialPoint",p)
        self.add_hook("upperInitialPoint",r)
        if polyline:
            self.intersected_by(Prism.from_polyline_vector(polyline.translate(-10000*Z),20000*Z))




def WoodStud(dimx,dimy,dimz,grainVector=Z,texture=None):
    if texture is None:
        texture=Texture("DMFDarkOak scale .03")
    c=Cube.from_dimensions(dimx,dimy,dimz)
    M=Map.rotational_difference(Z,grainVector)    
    c.new_texture(texture)
    c.texture.move(M)
    return c

def RoundedWoodStud(dimx,dimy,dimz,radius=.005,grainVector=Z,texture=None):
    if texture is None:
        texture=Texture("DMFDarkOak scale .03")
    c=RoundBox.from_dimensions(dimx,dimy,dimz,radius)
    c.new_texture(texture)
    M=Map.rotational_difference(Z,grainVector)
    c.texture.move(M)
    return c

def WoodBoard(xdim,ydim,thickness,xnumber=2,grainVector=Z,texture=None):
    """ 
    returns a board in the xy plane obtained by tiling in the x direction
    """
    if texture is None:
        texture=Texture("DMFDarkOak scale .03")
    c=RoundedWoodStud(xdim,ydim,thickness,radius=.005,grainVector=grainVector,texture=texture)
    return c#Tiling(c,jointWidth=-.0001,jointHeight=0,xnumber=xnumber,ynumber=1,polyline=None)

def PictureFrame(xdim,ydim,thickness,borderWidth,radius=.005):
    l1=RoundedWoodStud(xdim,borderWidth,2*thickness,radius=radius,grainVector=X)
    l3=l1.copy().translate((ydim-borderWidth)*Y)
    l2=RoundedWoodStud(borderWidth,ydim,2*thickness,radius=radius,grainVector=Y)
    l4=l2.copy().translate((xdim-borderWidth)*X)
    plane1=plane.from_3_points(origin,origin+Z,origin+X+Y)
    if plane1.half_space_contains(origin+X):
        plane1.reverse()
    l1.amputed_by(plane1)
    l2.amputed_by(plane1.copy().reverse())
    plane1.translate(l3.point(1,1,1,"ppp")-origin)
    l4.amputed_by(plane1)
    l3.amputed_by(plane1.copy().reverse())
    plane2=plane.from_3_points(origin,origin+Z,origin-X+Y)
    if plane2.half_space_contains(origin+X+Y):
        plane2.reverse()
    plane3=plane2.copy().translate(xdim*X)
    plane2.translate(ydim*Y)
    l2.amputed_by(plane2.copy().reverse())
    l3.amputed_by(plane2)
    l1.amputed_by(plane3.copy().reverse())
    l4.amputed_by(plane3)
    ret=Compound()
    ret.add_list_to_compound([l1,l2,l3,l4])
    ret.add_box("globalBox",Cube(origin,origin+xdim*X+ydim*Y+thickness*Z).box())
    return ret

def FramedGlass(width,height,thickness,borderWidth):
    mape=Map.linear(X,Z,Y)
    border=PictureFrame(width,height,thickness,borderWidth).move(mape)
    glass=Cube(origin,origin+(width-2*borderWidth)*X+(height-2*borderWidth)*Z+.002*Y)
    glass.new_texture("Glass")
    glass.translate(border.center-glass.center)
    ret=Compound()
    ret.add_list_to_compound([["frame",border],["glass",glass]])
    ret.add_box("globalBox",border.box())
    return ret

def CabinetStorey(b0,b1,b2,b3):
    """
    creates a storey for a cabinet from 4 boeards. The 4 boards are in the (x,z) plane and parallel
    and the outside face of the board is oriented towards the negative y. 
    This function gives the right orientation to the 4 boards and returns a compound with 4 panels 
    called front,irght,back,left, and a box. Each board must have a box for the computations to occur. 
    """
    b0.named("b0")
    b1.rotate(Z,math.pi/2).named("b1")
    b2.rotate(Z,math.pi).named("b2")
    b3.rotate(Z,-math.pi/2).named("b3")
    for ob in [b0,b1,b2,b3]:
        ob.add_hook("bottomFrontLeft",ob.point(0,0,0,"ppp"))
        ob.add_hook("bottomFrontRight",ob.point(1,0,0,"ppp"))
    for pair in [[b0,b1],[b1,b2],[b2,b3]]:
        pair[0].select_hook("bottomFrontRight")
        pair[1].select_hook("bottomFrontLeft")
        pair[1].hooked_on(pair[0])
    c=Compound()
    c.add_list_to_compound([["front",b0],["right",b1],["back",b2],["left",b3]])
    d=Cube(b0.point(0,0,0,"ppp"),b1.point(1,0,1,"ppp"))
    #print(b1[0])
    c.add_box("globalBox",d.box())
    return c

def Drawer(dimx,dimy,dimz,thickness):
    b0=WoodBoard(dimx,thickness,dimz-thickness,grainVector=X)
    b2=b0.copy()
    b1=WoodBoard(dimy,thickness,dimz-thickness,grainVector=X)
    b3=b1.copy()
    c=CabinetStorey(b0,b1,b2,b3)
    b=WoodBoard(dimx,dimy,thickness,grainVector=Y)
    c.above(b)
    ret=Compound()
    ret.add_list_to_compound([b,c])
    return ret



            
""" 
TODO
* revoir et reautomatiser la doc
* ajouter le thick triangle
* debugger le plan qui n'est pas bouge' proprement par une action non orthogonale
* ajouter des objets : 2 armoires, \'etagere, carrelage, interrupteurs 
bouger la chair avec un above comme la table. 
* ajouter le prisme et le polygone,le wall, la Room,fenetres a la doc, la librairie archi, la rounded box, 
le torus
dire que above marche avec des points dans la doc,doc des hooks, des lampes, des couleurs.
doc sur les textures.  
"""
