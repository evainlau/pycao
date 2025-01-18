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


import numpy as np
#import bpy
import math
from math import *
import sys,os
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac

from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *



class Compound(ElaborateOrCompound):
    """
    A class for objects for compound objects, which share a move_alone function 
    """
    def __new__(cls,*args,**kwargs):
        #print("DANS NEW compound")
        comp=ElaborateOrCompound.__new__(cls,*args,**kwargs)
        csgOperation=Object()
        csgOperation.csgKeyword="union"
        csgOperation.csgSlaves=[]
        comp.csgOperations=[csgOperation]
        return comp
        
    def __init__(self,slavesList=[]):
        """
        Each entry of  slavesList is
        - an object in World with no genealogy
        - or a sublist [name,objectInworld], where name is a string. 
        In the second case, the subobject will be accessible with self.name
        """
        #ObjectInWorld.__init__(self)
        for slave in slavesList:
            #print("avantAJout")
            self.add_to_compound(slave)
            #print("apresAJout")

    def add_to_compound(self,slave):
        "add a slave to the compound where slave is an objectInWorld or a list [name,ObjectInWorld]"
        if isinstance(slave,ObjectInWorld):
            #print("avantAjoutindiv")
            self.csgOperations[0].csgSlaves+=[slave]
            #print("apresAjoutIndiv")
        else :
            name=slave[0]
            slave=slave[1]
            setattr(self,name,slave)
            self.csgOperations[0].csgSlaves+=[slave]
        slave.parent=self# not really correct. The purpose is to not include this twice in camera.filmallactors
    def add_list_to_compound(self,myList):
        for ob in myList:
            self.add_to_compound(ob) 
        return self


            
    def print_slaves(self):
        print(self.__dict__)
        print(self.csgOperations[0].csgSlaves)
        
    def move_alone(self,mape):
        """
        the obect o is a compound iff o admits a union in its list of csg operations iff o has a unique union in its csg operations
        and this union is the first item. """
        #self.mapFromParts=mape*self.mapFromParts
        slaves=self.csgOperations[0].csgSlaves
        for slave in slaves:
            slave.move(mape,topLevel=False)
        return self

        
    def build_from_slaves(self):
        Compound.__init__(self,slavesList=self.slaves)

    def __str__(self):
        self.print_slaves()
        return "This is a compound"

    # def colored(self,string):
    #     slaves=self.csgOperations[0].csgSlaves
    #     for slave  in slaves :
    #         slave.colored(string)
    #     return self
    
class Lathe(Elaborate):
    """
    Class for Lathe objects
    By default, the Lathe occurs around the Y-axis
    The curve is assumed to have points of the form [x,y,0] with x>0
    If not, the control points are projected to get z=0
    """
    def __init__(self,curve):
        #  and the Lathe is around the Y axis.
        self.parts=Object()
        self.parts.curve=curve
        self.markers=Object()
        self.markers.box=FrameBox(listOfPoints=[eachPoint for eachPoint in curve ])
        self.markers_as_functions()
        #self.move_alone(Map.affine(X,Z,Y,origin)) Bad idea, need to conjugate if I want to change the axis
    @staticmethod
    def fromPolyline(curve):
        return Lathe(curve)
    @staticmethod
    def fromBezierCurve(curve):
        # To be printable by povray, the curve must have four points 
        return Lathe(curve)
    @staticmethod
    def fromPiecewiseCurve(curve):
        #  all the y components of the curve need  to be positive. 
        return Compound([Lathe(c) for c in curve])

    




class FrameAxis(Compound):
    """
    Class for 'arrows', ie. cylinder+cone at the end.

    Constructor:
    FrameAxis(start,end,cylinderPercentage,cylinderRadius,arrowRadius) : start,end=points for the extremities of the arrow. CylinderPercentage: the portion 
    of the arrow filled by the cylinder( the reminder being filled by the cone). 

    """
    def __init__(self,start,end,cylinderPercentage,cylinderRadius,arrowRadius):
        start=start.clone()
        end=end.clone()
        endCylinder=(1-cylinderPercentage)*start+cylinderPercentage*end
        cyl=Cylinder(start,endCylinder,cylinderRadius)
        #cyl.color=color
        cone=Cone(endCylinder,end,arrowRadius,0)
        #cone.color=color
        self.slaves=[["cyl",cyl],["arrow",cone]]
        self.build_from_slaves()


class BentCylinder(Compound):
    """
    A class for BentCylinders, similar to obects obtained from a Cylindric tube and a bending machine. Technically, this is 
    a succession of cylinders, and SlicedTorus. 

    Constructor
    BentCylinder(listOfPoints,radius,startWithTorus=False):
    if startWithTorus==True, the first piece is a sliced Torus, otherwise the first piece is a cylinder.
    The radius argument is both the radius of the Cylinder and the small radius of the torus. 
    The list of points =[p0,p1,,,,pn] is such that p0 is the starting point of the
    first piece, pn is the ending point of the last piece, p1,...p(n-1) are the junction points between the pieces.
    The large radius, normal and center of the torus are automatically computed from the data. 
    If n==1 and startWithTorus==True, an error is raised as the mathematical problem of determining the torus is not feasible.  
    """
    def __init__(self,listOfPoints,radius,startWithTorus=False):
        # construction des tangentes
        tangents=[]
        if not startWithTorus:
            for i in range(len(listOfPoints)-1):
                if i % 2==0:
                    tangents.append(listOfPoints[i+1]-listOfPoints[i])
                else:
                    tangents.append(listOfPoints[i]-listOfPoints[i-1])
        else:
            for i in range(1,len(listOfPoints)-1):
                if i % 2== 1:
                    tangents.append(listOfPoints[i+1]-listOfPoints[i])
                else:
                    tangents.append(listOfPoints[i]-listOfPoints[i-1])
            # it remains to compute the first tangent
            c=Circle.from_2_points_and_tangent(listOfPoints[1],listOfPoints[0],tangents[0])
            mape=Map.rotational_difference(listOfPoints[1]-c.center,listOfPoints[0]-c.center)
            tangents=[tangents[0].clone().remove_children().move_alone(mape)]+tangents
        # Now I add the last tangent
        oddNumberOfPoints= (len(listOfPoints)% 2 == 1)
        endWithCylinder=( startWithTorus == oddNumberOfPoints)
        nbp=len(listOfPoints)
        if endWithCylinder:
            tangents.append(listOfPoints[nbp-1]-listOfPoints[nbp-2])
        else:
            c=Circle.from_2_points_and_tangent(listOfPoints[nbp-2],listOfPoints[nbp-1],tangents[nbp-2])
            mape=Map.rotational_difference(listOfPoints[nbp-2]-c.center,listOfPoints[nbp-1]-c.center)
            tangents.append(tangents[nbp-2].clone().remove_children().move_alone(mape))
        # construction du slave(start,tangentStart,end,tangentEnd)
        def buildSlave(start,tangentStart,end,tangentEnd):
            if tangentStart==tangentEnd:
                return Cylinder(start,end,radius)
            else:
                c=Circle.from_2_points_and_tangent(start,end,tangentStart)
                torus=Torus(c.radius,radius,c.plane.normal,c.center)
                acute=(((start-c.center).cross(tangentStart)).dot((start-c.center).cross(end-c.center))>=0)
                # There may be problems if start and end are opposite points of the circle
                if np.allclose(end+start,2*c.center):
                    precision=10**(-5)
                    deviation=precision*c.plane.normal.cross(end-start)
                    end=end+deviation
                    #print("little change")
                torus.sliced_by(start,end,acute)
                return torus
        self.slaves=[]
        for i in range(len(listOfPoints)-1):
            self.slaves.append([str(i),buildSlave(listOfPoints[i],tangents[i],listOfPoints[i+1],tangents[i+1])])
        self.build_from_slaves()

    @staticmethod
    def from_polyline(listOfPoints,curvatureRadius,tubeRadius):
        """
        Returns a bent cylinder obtained from a polyline. First, the polyline is modified 
        with the replacement of each angle by an arc of circle with radius curvatureRadius.
        The curve obtained is a sequence of lines and arc or circles. Finally, cylinders and 
        slices of tori are drawn along this curve. 
        
        The construction is not possible and the results are inconsistent visually if the curvatureRadius is too large. 
        The precise condition is that if a and b are the angles at the vertexes of a segment of the polyline, then
        length(segment)/(tan(a/2)+length(segment)/tan(b/2))>curvatureRadius. This is the condition for the end of the last portion of the torus not 
        to interfere with the beginning of the next torus. On the first and last segment, there is a unique angle a and the 
        condition is tan(a/2)<length(segment)/curvatureRadius, otherwise the circle is too large to fit in the angle. 

        constructor
        BentCylinder.from_polyline(listOfPoints,curvatureRadius,tubeRadius)
        The points in the list are described by absolute coordinates (as a point) or by a coordinate relative to the previous point (as a vector).
        The previous point is the origin by definition for the first point in the list. 
        Example: [origin,X,Y] is equivalent to [origin,origin+X,origin+Y]
        """

        # I start to construct the absolute list of the polyline from the possible relative list
        def cotan(x):
            return math.cos(x)/math.sin(x)
        spline_=Polyline(listOfPoints)
        anglesList=[math.pi]+spline_.angles()+[math.pi]
        lengthsList=spline_.lengths()
        possibleRadius=[]
        for i in range(len(spline_)-1):
            #print("length,anglei,anglei+1")
            #print(lengthsList[i])
            #print(anglesList[i]/3.14)
            #print(anglesList[i+1]/3.14)
            #print(tan(0.5*anglesList[i]))
            #print("radius")
            #print ()
            possibleRadius.append((1.*lengthsList[i]*cotan(0.5*anglesList[i])+lengthsList[i]*cotan(0.5*anglesList[i+1])))
        #print("possRadius",possibleRadius)
        #print min(possibleRadius)
        if  min(possibleRadius)<curvatureRadius:
            raise NameError("The curvatureRadius is too large and not compatible with the angles and lengths of the segments")
        #for i in range(len(spline_-2)
        # Now I build the bentCylinder list of points from the polyline list of Points 
        bentList=[spline_[0]]
        for i in range(1,len(spline_)-1):
            c=Circle.from_tangent_triangle(Triangle(spline_[i-1],spline_[i],spline_[i+1]),curvatureRadius)
            bentList.append(c.contact[0])
            bentList.append(c.contact[1])
        bentList.append(spline_[-1])
        #for point in bentList:
        #    print(point)
        retour=BentCylinder(bentList,tubeRadius)
        retour.spline=spline_
        #print (retour.spline)
        return retour


class ThickTriangle(Compound):
    """
    retruns a thick triangle whose 3 vertices are spheres of radius r1,r2,r3. This is an oriented triangle with a normal.
    Optional parameters rn and rnn (n for normal and nn for non normal) are float. They are used to cut with a plane 
    on the normal side at distance rn of the plane containg the 3 vertices and parallel to ( resp. at distance rnn on the other side). 
    """
    def __init__(self,p1,p2,p3,r1,r2,r3,rn=None,rnn=None,pointOrVectorOnNOrmalSide=None):
        myplane=plane.from_3_points(p1,p2,p3)
        if pointOrVectorOnNOrmalSide is None:
            normal=myplane.normal.normalized_clone()
        s1=Sphere(p1,r1)
        s2=Sphere(p2,r2)
        s3=Sphere(p3,r3)
        p1n=p1+r1*normal
        p1nn=p1-r1*normal
        p2n=p2+r2*normal
        p2nn=p2-r2*normal
        p3n=p3+r3*normal
        p3nn=p3-r3*normal
        planen=plane.from_3_points(p1n,p2n,p3n)
        planenn=plane.from_3_points(p1nn,p2nn,p3nn)
        plane12=plane.from_3_points(p1n,p1nn,p2)
        plane13=plane.from_3_points(p1n,p1nn,p3)
        plane23=plane.from_3_points(p2n,p2nn,p3)
        
        plane122=plane(p2-p1,p1)
        plane211=plane(p1-p2,p2)
        plane133=plane(p3-p1,p1)
        plane311=plane(p1-p3,p3)
        plane233=plane(p3-p2,p2)
        plane322=plane(p2-p3,p3)
        s1.intersected_by([plane122,plane133,planenn,planen])
        s2.intersected_by([plane211,plane233,planenn,planen])
        s3.intersected_by([plane322,plane311,planenn,planen])
        if not planen.half_space_contains(p1nn):
            planen.reverse()
        if not planenn.half_space_contains(p1n):
            planenn.reverse()
        if not plane12.half_space_contains(p3):
            plane12.reverse()
        if not plane13.half_space_contains(p2):
            plane13.reverse()
        if not plane23.half_space_contains(p1):
            plane23.reverse()
        c12=Cone(p1,p2,r1,r2)
        c13=Cone(p1,p3,r1,r3)
        c23=Cone(p2,p3,r2,r3)
        polyhedral=planen.intersected_by([planenn,plane12,plane13,plane23])

        Compound.__init__(self,[])
        for string in ["s1","s2","s3","polyhedral","c12","c13","c23","normal","plane12","plane13","plane23"]:
            self.add_to_compound([string,eval(string)])
        for slave in planen.csgOperations[-1].csgSlaves: #POUR preservers les couleurs
            self.add_to_compound(slave)
#        print(plane12,plane13,plane23,planen,planenn)
