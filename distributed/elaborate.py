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


    def __new__(cls,*args,**kwargs):
        #print("dans new")
        #print(cls)
        #print(isinstance(cls,ObjectInWorld))
        instance=ObjectInWorld.__new__(cls,*args,**kwargs)
        return instance

    def marker_method(self,marker):
        return copy.deepcopy(getattr(self.markers,marker)).move_alone(self.mapFromParts)
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
        self.markersList=[ a for a in dir(self.markers) if not a.startswith('__')]
        #print (self.markersList)
        for marker in self.markersList:
            #print(marker)
            setattr(self.__class__,marker,Elaborate.fixing_param(marker,Elaborate.marker_method))



            #return self

    def copy(self):
        #return super(ElaborateOrCompound).__deepcopy__(self).markers_as_functions()
        #print (self.csgOperations)
        a=copy.deepcopy(self)
        #print(a.csgOperations)
        #print (self.csgOperations)
        #a.markers_as_functions()
        #print (self.csgOperations)
        return a


class Elaborate(ElaborateOrCompound):
    def move_alone(self,mape):
        self.mapFromParts=mape*self.mapFromParts
        return self


    

class Prism(ElaborateOrCompound):
    def __init__(self,polyline1,polyline2,
                 splineType="linear",sweepType="linear"):
        """A class for prisms.

        Constructor
        upperPolyline,lowerPolyline: a sequence of points in absolute or relative coordinates. Only the x,z coordinates are meaningful for the construction.
        height1, height2: heights for lower and upper polyline respectivly
        splineType=linear ( to be implemented in future:  quadratic or cubic or bezier for the interpolation between points)
        sweepType=linear ( to be implemented : conic. With conic only one height is sufficient (see povray doc). )
        """
        self.splineType=splineType
        self.sweepType=sweepType
        self.polyline1=Polyline(polyline1)
        if (self.polyline1[0] != self.polyline1[-1]).any():
            raise NameError("The first and last point of the underlying splines must be equal in a prism")
        self.polyline2=Polyline(polyline2)
        if (self.polyline2[0] != self.polyline2[-1]).any():
            raise NameError("The first and last point of the underlying splines must be equal in a prism")
        self.povrayNumberOfPoints=len(polyline1)
        
    def height(self,i):
        """
        Returns the y coordinate of the first point of spline number i, which is intended to be used as height
        """
        if i==1:
            return self.polyline1[0][1]
        elif i==2:
            return self.polyline2[0][1]
        else:
            raise NameError('Wrong parameter "i" for Prism.height(i)')


    
class Cylinder(Elaborate,BoundedByBox):
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
        start2=copy.deepcopy(start)
        end2=copy.deepcopy(end)
        if start2 is None:
            start2=point(0,0,-length/2)
            end2=point(0,0,length/2)
        # self.parts
        self.parts=Object()
        self.parts.start=start2
        self.parts.end=end2
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



class ICylinder(Elaborate):
    """
    Class for infinite cylinders

    Attributes:
    self.radius : the radius at the time of creation
    self.segment() 

    
    """
    def __init__(self,axis,radius):
        """
        If start is not None, self is computed from start,end,radius.
        If start is None, self is computed from length and radius : it is a cylinder with axis = Z
        and centered on zero.
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
       #print(type(eCylinder))
        return eCylinder
    def __str__(self):
        return ("Washer with radius "+str(self.parts.radius)+" and "+str(self.internalRadius) + " and axis "+str(self.axis()))





class Torus(Elaborate,BoundedByBox):
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
    def __str__(self):
        return ("Torus with center "+str(self.center)+" normal "+str(self.normal())+" radius "+str(self.parts.externalRadius)+","+str(self.parts.internalRadius))


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
        return self

    @staticmethod
    def from_circle_and_radius(circle,internalRadius):
        return Torus(circle.radius,internalRadius,circle.plane.normal,circle.center)


class Cube(Elaborate,BoundedByBox):
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
            self.markers.box=FrameBox(listOfPoints=[self.parts.start,self.parts.end])
            self.markers_as_functions()
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
    def __str__(self):
        string="Cube with corners "+str(self.start())+" and "+str(self.end())
        return string


class Sphere(Elaborate,BoundedByBox):
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
            self.parts.center=args[0]
            self.parts.radius=float(args[1])
        elif len(args)==4:
            self.parts.center=point(args[0],args[1],args[2])
            self.parts.radius=float(args[3])
        else:
            raise('Wrong Number of Arguments to create a Sphere')
        self.markers.box=FrameBox(listOfPoints=[self.parts.center-self.parts.radius*vector(1,1,1),self.parts.center+self.parts.radius*vector(1,1,1)])
        self.markers_as_functions()




        

class Cone(Elaborate,BoundedByBox):
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

        # The cone and its handles are  built from the following data: vectorAxis,center1,center2,length,radius2,radius1
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
        Les handles seront le debut du tube, le debut et la fin de chaque morceau de cercle, et enfin la fin du tube. 
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
        #print("angles",angles)
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
            self.add_handle(name=str(i)+"_"+str(coordonneesHandles[i]),coordinates=coordonneesHandles[i].to_3d(),visibility=0)
            #print (coordonneesHandles[i].to_3d())





class RuledSurface(Elaborate,BoundedByBox):
    """
    Constructs the mesh formed by the join of 2 parametrized curves C1,C2. By default, the discrete time t1  and t2 for the parametrization 
    is uniform on [0,1] but this is overridable by the parameters timeList. The mesh contains the triangles c1(t1(i)) c2(t2(i)) c2(t2(i+1))
    and  c1(t1(i)) c1(t1(i+1)) c2(t2(i+1))

    Constructors
    RuledSurface(curve1,curve2,timeList1=[],timeList2=[])
    RuledSurface.fromCurveFilling(curve1,stepNumber=6)

    markers
    box()
    """


    def __init__(self,curve1,curve2,timeStepsPerSegment=5,timeList1=[],timeList2=[]):
        numberOfIntervals=timeStepsPerSegment*(len(curve1)+len(curve2))
        if timeList1==[]:
            timeList1=[1.0*i/(numberOfIntervals) for i in range(numberOfIntervals+1)]
        if timeList2==[]:
            timeList2=[1.0*i/(numberOfIntervals) for i in range(numberOfIntervals+1)]
        self.parts=Object()
        self.parts.curve1=curve1
        self.parts.curve2=curve2
        self.parts.timeList1=timeList1
        self.parts.timeList2=timeList2

        #self.markers
        self.markers=Object()
        self.markers.box=FrameBox(listOfPoints=[curve1.atTime(t1) for t1 in timeList1]+[curve2.atTime(t2) for t2 in timeList2])
        self.markers_as_functions()
    def fromCurveFilling(curve,stepNumber=6)   :
        """
        Creates a ruled Surface  from a Closed curve by "filling the hole" with lines. The curve is divided into the first half C1 
        and the second halt C2. The ruled surface is the join between c1 and c2. 
        """
        
        
    def __str__(self):
        return ("Mesh for the Join of the curves "+str(curve1)+" and "+str(curve2))

    
