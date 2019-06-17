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

import copy
import numpy as np
import math
import sys,os
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac
import subprocess

from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *



class ElaborateOrCompound(ObjectInWorld):
    """
    A class for objects for elaborate objects, which share a move_alone function 
    """


    def marker_method(self,marker):
        memo={}
        return copy.deepcopy(getattr(self.markers,marker),memo).move_alone(self.mapFromParts)
#    def third_argument_with_selfAndMarker_fixed(self,marker,f):
#        def function_f_with_selfAndMarker_fixed():
#            return f(self,marker)
#        return function_f_with_selfAndMarker_fixed
    @staticmethod
    def fixing_param(marker,f):
        def function_f_with_marker_fixed(self):
           #print("le marqueur")
            #print(marker,self)
            #print(self)
            #print(getattr(self,marker))
            #print( f(self,marker))
            return f(self,marker)
        return function_f_with_marker_fixed
    def markers_as_functions(self):
        correctiveMap=self.mapFromParts.inverse()
        self.markersList=[ a for a in dir(self.markers) if not a.startswith('__')]
        #print (self.markersList)
        for marker in self.markersList:
            #print(marker, "etait le marqueur")
            setattr(self.__class__,marker,Elaborate.fixing_param(marker,Elaborate.marker_method))
            #setattr(self,marker,self.marker)

    def markers_as_functions2(self):#for debugging can be withdrawn
        correctiveMap=self.mapFromParts.inverse()
        self.markersList=[ a for a in dir(self.markers) if not a.startswith('__')]
        #print (self.markersList)
        for marker in self.markersList:
            #print(marker, "etait le marqueur")
            setattr(self.__class__,marker,Elaborate.fixing_param(marker,Elaborate.marker_method))
            #setattr(self,marker,self.marker)





class Elaborate(ElaborateOrCompound):
    def move_alone(self,mape):
        self.mapFromParts=mape*self.mapFromParts
        #print("dansMAl",self,mape,self.mapFromParts)
        return self


    

class Prism(Elaborate):
    def __init__(self,polyline1,height=1,splineType="linear",sweepType="linear"):
        """A class for prisms.

        Constructor
        polyline1=a polyline in a plane y=cte and all the points of the polyline are distinct
        returns the Prism with faces polyline1 and polyline1.translated(height *Y)
        splineType=linear ( to be implemented in future:  quadratic or cubic or bezier for the interpolation between points)
        sweepType=linear ( to be implemented : conic. With conic only one height is sufficient (see povray doc). )
        """
        self.splineType=splineType
        self.sweepType=sweepType
        self.polyline1=polyline1
        # suppressing the follwing 2 lines because of rounding pbs
        #if (self.polyline1[0] != self.polyline1[-1]).any():
        #    raise NameError("The first and last point of the underlying splines must be equal in a prism")
        self.height1=self.polyline1[0][1]
        self.height2=self.height1+height
        self.povrayNumberOfPoints=len(polyline1)

        
    @classmethod
    def from_polyline_vector(cls,polyline,vector):
        """ returns the prism B whose parallel faces are polyline and polyline+vector"""
        normalVec=polyline.normal()
        map1=Map.rotational_difference(normalVec,Y)
        map1Inverse=map1.inverse()
        intermediateVector=map1*vector        
        map2Inverse=Map.linear(X,intermediateVector,Z)
        map2=map2Inverse.inverse()
        composeMap=map2*map1
        composeMapInverse=map1Inverse*map2Inverse
        polyline1=polyline.copy().move(composeMap)
        p=Prism.__new__(cls,polyline1,height=1).move(composeMapInverse)
        Prism.__init__(p,polyline1)
        p.prismDirection=vector
        return p
        
class Cylinder(Elaborate):
    """
    Class for bounded cylinders

    Attributes:
    self.radius : the radius at the time of creation
    self.axis() 
    self.start()= an extremal point of the axis
    self.end()= the other extremal point of the axis

    
    """
    def __init__(self,start=None,end=None,radius=None,length=None,booleanOpen=False):
        """
        If start is not None, self is computed from start,end,radius.
        If start is None, self is computed from length and radius : it is a cylinder with axis = Z
        and centered on zero.
        """
        
        if radius is None:
            raise NameError('No default radius for a Cylinder')
        if start is None:
            start=point(0,0,-length/2)
            end=point(0,0,length/2)
        # self.parts
        self.parts=Object()
        self.parts.start=start
        self.parts.end=end
        self.parts.radius=radius
        self.parts.open=booleanOpen
        #self.markers
        self.radius=self.parts.radius
        self.markers=Object()
        self.markers.axis=Segment(self.parts.start,self.parts.end)
        self.markers.start=self.parts.start
        self.markers.end=self.parts.end
        M=Map.rotational_difference(Z,self.parts.end-self.parts.start)
        corner1=self.parts.start-self.parts.radius*M*(Y+X)
        corner2=self.parts.end+self.parts.radius*M*(Y+X)
        self.markers.box=FrameBox(listOfPoints=[corner1,corner2])
        self.markers_as_functions()
    @property
    def length(self):
        return (self.mapFromParts*(self.parts.end-self.parts.start)).norm
 
    def __str__(self):
        return ("Cylinder with extremal points "+str(self.start())+" and "+str(self.end()))

#    def __copy__(self,*args,**kwargs):
#        """
#        This stupid name to avoir an autorecursive deepcopy
#        """
    def __deepcopy__(self, memo):
        myCopy = Cylinder(start=self.start(),end=self.end(),radius=self.radius,length=None,booleanOpen=self.parts.open)
        memo[id(self)] = self
        for key in self.__dict__:
            toCopy=self.__dict__[key]
            myCopy.__dict__[key] = copy.deepcopy(toCopy,memo)
        return myCopy
    def __copy__(self):
        memo={}
        return self.deepcopy(memo)
    @staticmethod
    def from_point_vector(p,v,r):
        return Cylinder(p,p+v,r)
    
    
class ICylinder(Elaborate):
    """
    Class for infinite cylinders

    Attributes:
    self.radius : the radius at the time of creation
    self.segment() 

    
    """
    def __init__(self,axis,radius):
        """
        """
        if radius is None:
            raise NameError('No default radius for a Cylinder')
        # self.parts
        self.parts=Object()
        self.parts.axis=axis
        self.parts.radius=radius
        M=Map.rotational_difference(Z,self.parts.axis.vector)
        N=Map.affine(M*X,M*Y,M*Z,self.parts.axis.p1-origin)
        self.parts.mapFromParts=N
        self.mapFromParts=self.parts.mapFromParts
        #self.markers
        self.radius=self.parts.radius
        self.markers=Object()
        self.markers.segment=Segment(origin,origin+(self.parts.axis.p2-self.parts.axis.p1).norm*Z)
        self.markers_as_functions()

    def __str__(self):
        return ("Infinite Cylinder with radius "+str(self.parts.radius)+ " and axis "+str(self.axis()))

    @staticmethod
    def from_point_vector_radius_amputation(p,v,r):
        """
        Constructs a half cylinder with half line p+tv, t>0
        """
        l=Segment(p,p+v)
        return ICylinder(l,r).amputed_by(plane(v,p))
        

class HalfICylinder(ICylinder):
    """
    A class to produce half cylinders, aka ICylinders amputed by a plane
    """

    @staticmethod
    def from_point_vector_radius(p,v,radius):
        axis=Segment(p,p+v)
        cyl=ICylinder(axis,radius)
        toCut=plane.from_point_and_vector(axis.p1,axis.vector)
        cyl.amputed_by(toCut)
        return cyl

                        
class Washer(Cylinder):
    """
    A class for washers

    Markers:
    radius : externalRadius  at the time of creation
    externalRadius : an alias for radius
    internalRadius : at the time of creation
    box() the external box
    internalBox()
    start
    end
    axis
    
    Constructor
    Washer(start,end,eradius,iradius)
    """
    def __new__(cls,start,end,eradius,iradius):
        eCylinder=Cylinder.__new__(cls,start,end,eradius)
        Cylinder.__init__(eCylinder,start,end,eradius)
        iCylinder=Cylinder(start,end,iradius)
        longCylinder=ICylinder(Segment(start,end),iradius)
        #longCylinder.color=copy.copy(eCylinder.color)
        eCylinder.amputed_by(longCylinder)
        eCylinder.externalRadius=eCylinder.radius
        eCylinder.internalRadius=iCylinder.radius
        eCylinder.internalBox=iCylinder.box()
        eCylinder.markers_as_functions()
        return eCylinder

    def __str__(self):
        return ("Washer with radius "+str(self.parts.radius)+" and "+str(self.internalRadius) + " and axis "+str(self.axis()))





class Torus(Elaborate):
    """
    Class for tori. 

    Attributes:
    self.externalRadius : the radius at the time of creation
    self.internalRadius
    self.axis()
    self.normal()
    self.box() The y axis of the box is the axis of the torus
    self.center

    Constructor
    Torus(externalRadius,internalRadius,normal,center)
    
    
    """
    def __init__(self,externalRadius,internalRadius,normal=MassPoint(0,0,1,0),center=MassPoint(0,0,0,1)):
    #def __init__(self,*args,**kwargs):
        """
        The axis of rotation is Z by default and the center is the origin by default. 
        """
        # self.parts
        self.parts=Object()
        er=externalRadius
        ir=internalRadius
        self.parts.externalRadius=float(er)
        self.parts.internalRadius=float(ir)
        self.parts.normal=Y
        self.parts.center=origin
        self.mapFromParts=Map.rotational_difference(Y,normal,origin,center)
        #self.markers
        self.externalRadius=self.parts.externalRadius
        self.internalRadius=self.parts.internalRadius
        self.markers=Object()
        self.markers.axis=Segment(self.parts.center,self.parts.center+self.parts.normal)
        self.markers.box=FrameBox(listOfPoints=[point(-er-ir,-ir,-er-ir),point(er+ir,ir,er+ir)])
        self.markers.normal=self.parts.normal
        self.markers_as_functions()
    #def __deepcopy__(self,memo):
        
    def __str__(self):
        return ("Torus with center "+str(self.center)+" normal "+str(self.normal())+" radius "+str(self.parts.externalRadius)+","+str(self.parts.internalRadius))
    @staticmethod
    def from_3_points(start,middle,end,internalRadius,cut=True):
        """
        build a torus whose underlying circle goes through the 3 unaligned points in parameter. Self.curve will be the circle, parametrized 
        so that self.circle(0)=start and the orientation of the parametrization makes the circle goes from start to end, with middle in the middle 
        as time increases from 0. If cut is True, only the arc between start and end containing  middle are kept. 
        """
        plane1=Plane.from_2_points(start,middle)
        plane2=Plane.from_2_points(start,end)
        plane3=Plane.from_3_points(start,middle,end)
        normale=plane3.normal.normalize()
        center=Point.from_3_planes(plane1,plane2,plane3)
        delta=start-center
        radius=(start-center).norm
        vec1=(start-center).normalize()
        vec2=middle-center
        vec3=end-center
        angle1=vec1.angle_to(vec2,vaxis=normale)
        angle2=vec1.angle_to(vec3,vaxis=normale)
        if angle1<angle2:
            def circle_function(t):
                self.parametrizedPositivly=True # used in the copy process
                return start.rotate(axis=Segment(center,center+normale),angle=t)
        else:
            def circle_function(t):
                self.parametrizedPositivly=False
                return start.rotate(axis=Segment(center,center+normale),angle=-t)
        #creation du torus self
        self=Torus(radius,internalRadius,normale,center)
        self.circle=FunctionCurve(circle_function).glued_on(self)
        if cut is True:
            #print(normale)
            #print("center",center)
            cutting1=Plane.from_3_points(center,start,center+normale)
            cutting2=Plane.from_3_points(center,end,center+normale)
            #if center,start and end are aligned and we keep the half point containing middle
            #print(cutting1)
            #print(cutting2)
            if cutting1.is_parallel_to(cutting2):
                #print("parallel")
                if cutting1.half_space_contains(middle): 
                    return self.intersected_by(cutting1)
                else:
                    return self.intersected_by(cutting1.reverse())
            else:
                # I build the acute sector from start to end. 
                if not cutting1.half_space_contains(end):
                    cutting1.reverse()
                if not cutting2.half_space_contains(start):
                    cutting2.reverse()
            sector=cutting1.intersected_by(cutting2)
            #sector.colored("Yellow")
            #self.sector=cutting1
            if cutting1.half_space_contains(middle) and cutting2.half_space_contains(middle):
                return self.intersected_by(sector)
            else:
                return self.amputed_by(sector)
        else: return self



        
    def sliced_by(self,point1,point2,acute=True):
        """
        returns intersection/difference of a torus and a polyhedral P, where P is the intersection of 2 half spaces which meet along the axis of the torus

        Constructors:
        TorusSlice(torus,p1,p2,acute=True): The planes Pi for the polyhedral contain torusCenter,torusCenter+Normal,pi. The half space Pi contains the other point pj
        If acute is true, the constructor returns torus.intersected_by(polyhedral(P1,P2)) otherwise returns torus.amputed_by(polyhedral(P1,P2)) 
        
        """
        p1=point1.copy()
        p2=point2.copy()
        plane1=AffinePlaneWithEquation(self.center,self.center+self.normal(),p1)
        plane2=AffinePlaneWithEquation(self.center,self.center+self.normal(),p2)
        if not plane1.half_space_contains(p2):
            plane1.reverse()
        if not plane2.half_space_contains(p1):
            plane2.reverse()
        if 0.5*p1+0.5*p2==self.center: # here : one plane is enough, and 2 cause problems because of rounding numbers: the two planes may be opposite
            cuttingTool=[plane1]
        else:
            cuttingTool=[plane2,plane1]
        if acute:
            self.intersected_by(cuttingTool)
        else:
            result= self.amputed_by(Polyhedral(cuttingTool))
        plane1.disappears()
        plane2.disappears()
        return self

    @staticmethod
    def from_circle_and_radius(circle,internalRadius):
        return Torus(circle.radius,internalRadius,circle.plane.normal,circle.center)


class Cube(Elaborate):
    """
    builds a cube, ie a box with orthgonal edges parallel to the axis X,Y,Z
    
    Attributes:
    self.center()
    self.start()
    self.end()
    self.box: the FrameBox with the same dimensions as the cube
    self.dimensions() : the dimension of the box
    self.point(): returns a point in the box in appropriate coordinates (cf the doc of frameBox)

    Constructor:
    Cube(start,end), start,end are opposite corners of the Cube
    Cube(x,y,z) or Cube(vector(x,y,z)) x,y,z=the dimensions of the cube. Equivalent to Cube(origin,origin+vector(x,y,z))
    Cube(listOfPoints=[]) the smallestCube containing list of points
    """
    def __init__(self,*args,**kwargs):
        """
        """
        if len(args)==0 or len(args)>3:
            raise('Incorrect number of arguments to build a Cube')
        if len(args)==2:
            # self.parts
            self.parts=Object()
            self.parts.start=args[0]
            self.parts.end=args[1]
            # self.markers
            self.markers=Object()
            #self.markers.center=0.5*(self.parts.start+self.parts.end)
            self.markers.start=self.parts.start
            self.markers.end=self.parts.end
            #self.markers.box=FrameBox(listOfPoints=[self.parts.start,self.parts.end])
            self.add_box("globalBox",FrameBox(listOfPoints=[self.parts.start,self.parts.end]))
            #print("avantCreation Box")
            self.markers_as_functions()
            #print("apresCreaBox")
        elif len(args)==3:
            v=vector(args)
            self.__init__(origin,origin+v)
        elif is_vector(args[0]):
            self.__init__(origin,origin+args[0])
        else:
            xmax=max(coord[0]for coord in args[0])
            xmin=min(coord[0]for coord in args[0])
            ymax=max(coord[1]for coord in args[0])
            ymin=min(coord[1]for coord in args[0])
            zmax=max(coord[2]for coord in args[0])
            zmin=min(coord[2]for coord in args[0])
            # Now the coordinates of the two extreme corners in the base xDirection,yDirection,zDirection
            mini=point(xmin,ymin,zmin)
            maxi=point(xmax,ymax,zmax)
            self.__init__(mini,maxi)
    @staticmethod
    def from_dimensions(*args):
        if len(args)==3: return Cube(*args)
        if len(args)==1: return Cube(args(0),args(1),args(2))
    @staticmethod
    def from_list_of_points(listOfPoints):
        return Cube(listOfPoints)

        
    def __str__(self):
        string="Cube with corners "+str(self.start())+" and "+str(self.end())
        return string


class RoundBox(Elaborate):
    """
    builds a rounded cube, with orthgonal edges parallel to the axis X,Y,Z
    
    Attributes:
    self.center()
    self.box()
    self.dimensions() : the dimension of the box
    self.point(): returns a point in the box in appropriate coordinates (cf the doc of frameBox)

    Constructor:
    RoundBox(start,end,radius,merge), start,end are opposite corners of the Cube
    RoundBox(x,y,z,radius,merge)  
    """
    def __init__(self,*args,**kwargs):
        """
        """
        if len(args)<4 or len(args)>5:
            raise NameError('Incorrect number of arguments to build a RoundBox')
        if len(args)==4:
            # self.parts
            self.parts=Object()
            self.parts.start=args[0]
            self.parts.end=args[1]
            self.radius=args[2] #The radius at creation,may change with a non orthogonal map
            self.merge=args[3]
            # self.markers
            self.markers=Object()
            #self.markers.center=0.5*(self.parts.start+self.parts.end)
            self.markers.start=self.parts.start
            self.markers.end=self.parts.end
            self.markers.box=FrameBox(listOfPoints=[self.parts.start,self.parts.end])
            self.markers_as_functions()
        elif len(args)==5:
            point(args[0],args[1],args[2])
            self.__init__(origin,point(args[0],args[1],args[2]),args[3],args[4])
    @staticmethod
    def from_dimensions(x=1,y=1,z=1,radius=.1,merge=False):#an alias for code readability
        return RoundBox(x,y,z,radius,merge)
    @staticmethod
    def from_list_of_points(start=origin,end=point(1,1,1),radius=.1,merge=True):#an alias for code readability
        return RoundBox(start,end,radius,merge)

        
    def __str__(self):
        string="Rounded Cube with corners "+str(self.start())+" and "+str(self.end())
        return string

    

class Sphere(Elaborate):
    """
    Class for spheres

    Attributes: 
    self.center()
    self.radius : the radius at the time of creation
    self.box()

    Constructor:
    Sphere(center,radius) with radius=float and center=(x,y,z) or center=point(x,y,z)
    """
    def __init__(self,*args):
        self.parts=Object()
        self.markers=Object()
        if len(args)==2:
            self.parts.center=args[0].copy()
            self.parts.radius=float(args[1])
        elif len(args)==4:
            self.parts.center=point(args[0],args[1],args[2])
            self.parts.radius=float(args[3])
        else:
            raise('Wrong Number of Arguments to create a Sphere')
        self.markers.box=FrameBox(listOfPoints=[self.parts.center-self.parts.radius*vector(1,1,1),self.parts.center+self.parts.radius*vector(1,1,1)])
        self.markers_as_functions()




        

class Cone(Elaborate):
    """
    Constructors
    Cone(start,end,radius1,radius2)
    Cone(start,end,radius1,radius2,booleanOpen=True) : same cone as above, but with no caps at the extremities
    Cone(radius1,radius2,length)     Cone with axis z.  radius1 is at level z=-length/2, and radius2 at level z=length/2.
    Cone(radius1,radius2,length,booleanOpen=True)     Cone with axis z.  radius1 is at level z=-length/2, and radius2 at level z=length/2.

    Local coordinates :
    Ozloc parallel to the axis of the cone, 
    zloc=0 is the plane containing the circle of radius radius1
    zloc=1 in frame "p" is the plane containing the circle of radius radius2
    xloc=1 is a plane with distance max(radius1,radius2) from Oloc

    markers
    axis() : segment through the 2 extremal points on the axis. 
    box()
    radius1 : at the time of creation
    radius2 : at the time of creation
    """


    def __init__(self,*args,**kwargs):

        # The cone and its hooks are  built from the following data: vectorAxis,center1,center2,length,radius2,radius1
        # First, I compute these data from the arguments of the init function
        
        if len(args)==3:
            Cone.__init__(origin-0.5*args[2],origin+0.5*args[2],args[0],args[1])
        if len(args)==4:
            # self.parts
            self.parts=Object()
            self.parts.start=args[0]
            self.parts.end=args[1]
            self.parts.radius1=args[2]
            self.parts.radius2=args[3]
            try:
                self.parts.open=kwargs["booleanOpen"]
            except:
                self.parts.open=False
            #self.markers
            self.markers=Object()
            self.radius1=self.parts.radius1
            self.radius2=self.parts.radius2
            self.markers.axis=Segment(self.parts.start,self.parts.end)
            M=Map.rotational_difference(Z,self.parts.end-self.parts.start)
            radius=max(self.parts.radius1,self.parts.radius2)
            corner1=self.parts.start-radius*M*(Y+X)
            corner2=self.parts.end+radius*M*(Y+X)
            self.markers.box=FrameBox(listOfPoints=[corner1,corner2])
            self.markers_as_functions()
    def __str__(self):
        return ("Cone with extremal points "+str(self.axis().p1)+" and "+str(self.axis().p2)+" radius: "+str(self.radius1)+", "+str(self.radius2))

class Bobine(Cylinder):
    """
        TODO : complete rewriting necessary
    """

    def __init__(self,name,smallRadius=0,smallLength=0,largeRadius=0,largeLength=0,material=None):
        super(Bobine,self).__init__(name=name,radius=smallRadius,length=smallLength,material=material)
        self.topCover=Cylinder(name=name+"TopCover",radius=largeRadius,length=largeLength-smallLength,material=material)
        self.bottomCover=Cylinder(name=name+"BottomCover",radius=largeRadius,length=largeLength-smallLength,material=material)
        self.topCover.glued_on(self,"oom","ooM")
        self.bottomCover.glued_on(self,"ooM","oom")
        self.smallLength=smallLength
        self.smallRadius=smallRadius
        self.largeLength=largeLength
        self.largeRadius=largeRadius
        # ne pas effacer self.length ou self.radius car utilise' lors d'appels de fonctions heritees de Cylinder




class Screw(Elaborate):
    pass
        



class Bending2d(Elaborate):
    """

    """
    def __init__(self,name="",coordonnees=[],bendingRadius=10,tubeDiameter=1,subdivCardinal=10):
        """
        TODO : complete rewriting necessary


        coordonnees est une liste donnant les coordonnees 2D des points si on faisait une construction a base de tubes rectilignes: elle contient
        le debut, les points d'intersection des tubes et la fin. 
        Il existe un unique cercle de radius=bendingRadius et tangent a deux droites. La piece
        cintree qu'on veut considerer est celle qui est obtenue en remplacant chaque jonction/soudure 
        entre deux tubes rectilignes par un tube cintre' dont la forme est le
        cercle susdecrit. Chaque cercle est approxime' par subdivCardinal morceaux de droite. 
        Les hooks seront le debut du tube, le debut et la fin de chaque morceau de cercle, et enfin la fin du tube. 
        J'ai fait les calculs en supposant que les angles sont < a pi, sinon il faut sans doute changer les formules. 

        A bending tube is a sequence of objects O1,O2....
        such that:
        - Oi is a bounded cylinder or a portion of a torus
        - If Oi is a torus, Oi+1 is a cylinder and reciprocally
        - The cylinders and the torus have the same radius ( the small radius for the torus)
        - The end of the cylinder is the beginning of the next torus and reciprocally
        - The torus and the cylinders center are joined in a differentiable line ie the the circle of the torus is tangent to the
        lines of the cylinder which is after and before it. 


        Constructors: 
        Bending2d(radius,listOfJunctionPoints,listOfCenters,startWithCylinder=True,booleanOpen=False)
        Bending2d(polyline)
        """
        #print("coord",coordonnees)
        vecteurSuivant=[(coordonnees[i+1]-coordonnees[i]).normalized() for i in range(len(coordonnees)-1)]+["Pas defini"]
        #print("vecteurSuivant",vecteurSuivant)
        vecteurPrecedent=["Pas defini"]+[(coordonnees[i]-coordonnees[i-1]).normalized() for i in range(1,len(coordonnees))] 
        #print("vecteurPrecedent",vecteurPrecedent)
        angles=["pas d'angle defini en ce point"]+[-1*vecteurPrecedent[i].angle_signed(vecteurSuivant[i]) for i in range(1,len(coordonnees)-1
                                                                    )]+["pas d'angle defini en ce point"]
        distanceEntreHandles=[]
        pointsDuPolyline=[coordonnees[0]] 
        coordonneesHandles=[coordonnees[0]] 
        debutsDeCourbure={}
        finsDeCourbure={}
        #  construction des Points du spline, parmi lesquels les coordonnees des handles
        for i in range(1,len(coordonnees)-1):
            vecteurOrthogonal=Vector((-1*vecteurPrecedent[i][1],vecteurPrecedent[i][0]))
            petitAngle=angles[i]/subdivCardinal
            debutsDeCourbure[i]=coordonnees[i]-bendingRadius*abs(tan(angles[i]/2))*vecteurSuivant[i-1]
            finsDeCourbure[i]=coordonnees[i]+bendingRadius*abs(tan(angles[i]/2))*vecteurSuivant[i]
            coordonneesHandles.append(debutsDeCourbure[i])
            coordonneesHandles.append(finsDeCourbure[i])
            for j in range(subdivCardinal+1):
                pointsDuPolyline.append(debutsDeCourbure[i]+abs(sin(j*petitAngle))*bendingRadius*vecteurPrecedent[i]+(1-cos(j*petitAngle))*bendingRadius*(petitAngle)/abs(petitAngle)*vecteurOrthogonal)
        pointsDuPolyline.append(coordonnees[len(coordonnees)-1])
        coordonneesHandles.append(coordonnees[len(coordonnees)-1])
        super(Bending2d, self).__init__(name=name,createArguments=["Bending2d",name,pointsDuPolyline,tubeDiameter],description="") 
        #print("handles",coordonneesHandles)
        #print("pointsPolyline",pointsDuPolyline)
        for i in range(len(coordonneesHandles)-1):
            if (i%2==0): #les 2 handles sont separees par un tube rectiligne
                distanceEntreHandles.append((coordonneesHandles[i+1]-coordonneesHandles[i]).length)
            else: # les 2 handles sont reliees par un tube en form d'arc de cercle
                        distanceEntreHandles.append(abs(angles[(i+1)//2])*bendingRadius)
        #print("distanceHandles",distanceEntreHandles)
        for num in range(len(pointsDuPolyline)):  
            x, y = pointsDuPolyline[num]  
            polyline.points[num].co = (x, y, 0, 1) 
            #print("pointAjoute",(x,y,0,1))
        self.length=sum(distanceEntreHandles)
        #print("length",self.length)
        for i in range(len(coordonneesHandles)):
            self.add_hook(name=str(i)+"_"+str(coordonneesHandles[i]),coordinates=coordonneesHandles[i].to_3d(),visibility=0)
            #print (coordonneesHandles[i].to_3d())





class RuledSurface(Elaborate):
    """
    Constructs the mesh formed by the join of 2 parametrized curves C1,C2. By default, the discrete time t1  and t2 for the parametrization 
    is uniform on [0,1] but this is overridable by the parameters timeList. The mesh contains the triangles c1(t1(i)) c2(t2(i)) c2(t2(i+1))
    and  c1(t1(i)) c1(t1(i+1)) c2(t2(i+1))

    Constructors
    RuledSurface(curve1,curve2,openHole1=True,openHole2=True)
    RuledSurface.fromCurveFilling(curve1,stepNumber=6)

    markers
    box()
    """


    def __init__(self,curve1,curve2,quality=5):
        numberOfIntervals=int(quality**3)+2
        timeList1=[1.0*i/(numberOfIntervals) for i in range(numberOfIntervals+1)]
        timeList2=[1.0*i/(numberOfIntervals) for i in range(numberOfIntervals+1)]
        self.parts=Object()
        self.parts.curve1=curve1
        self.parts.curve2=curve2
        self.parts.timeList1=timeList1
        self.parts.timeList2=timeList2

        #self.markers
        self.markers=Object()
        self.markers.box=FrameBox(listOfPoints=[curve1.__call__(t1) for t1 in timeList1]+[curve2.__call__(t2) for t2 in timeList2])
        self.markers_as_functions()

            
    @staticmethod
    def fromCurveFilling(curve,quality=6)   :
        """
        Creates a ruled Surface  from a Closed curve by "filling the hole" with lines. The curve is divided into the first half C1 
        and the second halt C2. The ruled surface is the join between c1 and c2. 
        """
        firstHalf=curve.copy().reparametrize(lambda x:0.5*x)
        secondHalf=curve.copy().reparametrize(lambda x:0.5+0.5*x)
        return RuledSurface(firstHalf,secondHalf,quality=quality)
    
    def __str__(self):
        return ("Mesh for the Join of the curves "+str(curve1)+" and "+str(curve2))

    @staticmethod
    def fromJoinAndCaps(curve1,curve2,quality=5,cap1=True,cap2=True):
        slaves=[RuledSurface(curve1,curve2,quality)]
        if cap1:
            slaves.append(RuledSurface.fromCurveFilling(curve1,quality))
        if  cap2:
            slaves.append(RuledSurface.fromCurveFilling(curve2,quality))
        from compound import Compound
        return Compound(slaves)

            

    
def to_visualize_curves(self,radius=0.1,steps=100,color="Yellow",color2="Green"):
    """ 
    constructs spheres along the curve to visualize it. 
    Arguments:
    steps: The number of spheres 
    color: the color of the spheres 
    radius: the radius of the spheres
    color2: the color to mark the input points which are interpolated by the curve 
    """
    for time in range(0,steps,1):
        p=self(1./steps*time)
        s=Sphere(p,radius)
        s.color=color
        s.glued_on(self)
    if self.__class__== Polyline or self.__class__== BezierCurve:
        for point in self:
            s=Sphere(point,2*radius)
            s.color=color2
            s.glued_on(self)

ParametrizedCurve.show=to_visualize_curves
