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
import scipy
import scipy.special
from scipy.special import binom
import math
from math import *
import sys
import os
import copy
import types
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac

from uservariables import *
from generic import *



################################################################
"""
                Constructions of classes which define our mathematical framework:
                - Primitive : for primitive objects
                - MassPoint for elements in the massic space
                - Base for basis in the massic space 

"""
################################################################

class Primitive(ObjectInWorld):
    def copy(self):
        #print("in copy prim")
        #return super(ElaborateOrCompound).__deepcopy__(self).markers_as_functions()
        #print (self.csgOperations)
        memo={}
        a=copy.deepcopy(self,memo)
        #print(a.csgOperations)
        #print (self.csgOperations)
        #print (self.csgOperations)
        return a



class MassPoint(np.ndarray,Primitive):
    """
    Class for Mass points. 

    Construction
    myPoint=MassPoint(a,b,c,d) or myPoint=MassPoint([a,b,c,d])
    Point.from_3_planes(p0,p1,p2): the intersection of the 3 planes
    Point.from_plane_and_line(p,l): the intersection of p and l
    Point.from_2_lines(l1,l2):  returns the point in the second line closest to the first line. The 2 lines are supposed not parallel. 


    """
    # __methods__

    def __new__(cls, *args, **kwargs):
        l=list(args)
        l=[float(entry) for entry in l]
        return np.array(l).view(cls)

    def __init__(self,*args,**kwargs):       
        ObjectInWorld.__init__(self)
        pass
        
    def __array_finalize__(self,*args,**kwargs):
        ObjectInWorld.__init__(self)

    def copy(self):
        memo=dict()
        return self.__deepcopy__(memo)
        
    def __deepcopy__(self,memo):
        # I have to rewrite this because ndarray.deepcopy applies and forgets to copy the arguments
        result=MassPoint(self[0],self[1],self[2],self[3])
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
        
    def roundResult(masspoint):
        if math.fabs(masspoint[3])<0.000000001: masspoint[3]=0.
        if math.fabs(masspoint[3]-1)<0.000000001: masspoint[3]=1.
        return masspoint

    def __str__(self):
        try:
            if (self[3]==0):
            #return("Vector  "+np.ndarray.__str__(self[0:3]))
            # changed from the line above since it created a mass point with 3 entries
                return("Vector  ["+str(self[0])+","+str(self[1])+","+str(self[2])+"]")
            elif (self[3]==1):
                return("Affine Point  ["+str(self[0])+","+str(self[1])+","+str(self[2])+"]")
            else:
                return "Mass Point  "+np.ndarray.__str__(self)
        except:
            return "A Mass point with less than 4 entries, probably an automatic creation of numpy internal"
            
    def __eq__(self,other):
        return isinstance(other,MassPoint) and np.ndarray.all(np.equal(self,other))
  

    def __add__(self,other):
        if isinstance(other, MassPoint ):
            result=np.ndarray.__add__(self,other).view(MassPoint)
           
            
            ObjectInWorld.__init__(result)
            return result.roundResult()
        else :
            raise NameError('Unsupported addition for Mass point and'+str(type(other)))

    def __sub__(self,other):
        """
        Add two mass points, the result being a mass point of the sum of the 2 weights. 
        """
        if isinstance(other, MassPoint ):
            resul=np.ndarray.__sub__(self,other)
            result=MassPoint(resul[0],resul[1],resul[2],resul[3])
            #ObjectInWorld.__init__(result)
            return result.roundResult()
        else :
            #print(isinstance(other, MassPoint ))
            raise NameError('Unsupported difference for mass point point and'+str(type(other)))

#    def __mul__(self,other):
#        """
#        Multiplies self by a constant
#        """
#        if isinstance(other, float ):
#            result=np.ndarray.__mul__(self,other).view(MassPoint)
#            ObjectInWorld.__init__(result)
#            return result
#        else :
#            #print(isinstance(other, MassPoint ))
#            raise NameError('Unsupported difference for mass point point and'+str(type(other)))




    def cross(self,other):
        """
        Returns the cross product of self and other, which are vectors
        """
        if self[3]==0 and other[3]==0:
            #result=
            return vector(np.cross(self[0:3],other[0:3]))
        else:
            print(self)
            print(other)
            raise NameError("Cross product applies only to vectors")


                          
    def dot(self,other):
        """
        returns the scalar product self and other. 
        """
        if self[3]==0 and other[3]==0:
                    return np.dot(self,other)
        else:
            raise NameError("Scalar product applies only to vectors")


        
    @property
    def norm(self):
        if self[3]==0:
            return np.linalg.norm(self,2)
        else:
            #print("self",self)
            raise NameError('norm is applied to a Vector, self is '+str(type(self)))

    def normalized_copy(self):
        """ returns a vector positivly proportional to self with norm 1 """
        if self[3]==0:
            return 1./self.norm*self
        else:
            #print("self",self)
            raise NameError('norm is applied to a Vector, self is '+str(type(self)))

    def normalize(self):
        """ transforms self in a vector positivly proportional to self with norm 1, and returns it """
        if self[3]==0:
            if self.norm==0: raise ("Cannot Normalize the zero Vector")
            result=1./self.norm*self
            self[0:3]=result[0:3]
            return self
        else:
            #print("self",self)
            raise NameError('norm is applied to a Vector, self is '+str(type(self)))

    def angle_to(self,goal,vaxis):
        cosine= np.dot(goal,self)/np.linalg.norm(self)/np.linalg.norm(goal) # -> cosine of the angle
        angle = np.arccos(np.clip(cosine, -1, 1))
        M=Map.linear_rotation(vaxis,angle)
        toVanish=M*self.normalized_copy()-goal.normalized_copy() # it is zero if the angle is correct, and with norm 2|sin(angle)| otherwise
        if toVanish.norm>math.fabs(math.sin(angle)):
            angle=angle+math.pi
        return angle
    # other methods


    def move_alone(self,M):
        #print("selfInMA",self,M)
        self[:]=M*self
        return self


    def is_origin(self):
        return self[0]==0 and self[1]==0 and self[2]==0


    def projection_on_line(self,l):
        if self[3]==1:
            return Point.from_point_and_line(self,l)
        else: raise NameError('The projection is a applied to a point')


class Point(object):
    """
    A class to generate a point from different input data

    """
    def __new__(cls,x,y,z):
        return (MassPoint(x,y,z,1))

    @staticmethod
    def from_3_planes(p0,p1,p2):
        """
        returns a point as an intersection of 3 planes
        """
        matrix = np.array([p0[0:3],p1[0:3],p2[0:3]])
        b = np.array([-1.*p0[3],-1.*p1[3],-1.*p2[3]])
        x = np.linalg.solve(matrix, b)
        #print(p0)
        return point(x[0],x[1],x[2])

    @staticmethod
    def from_plane_and_line(p,l):
        """
        """
        a=p.evaluate_on(l.p1)
        b=p.evaluate_on(l.p2)
        step=b-a
        if a==0:
            return l.p1
        else:
            return l.p1-1.*a/step*l.vector
        
    @staticmethod
    def from_2_lines(l1,l2):
        """
        returns the point in the first line closest to the second line. In particular, if the 2 lines 
        intersect, this is the intersection. The 2 lines are supposed not parallel. 
        """
        p=AffinePlaneWithEquation.from_2_vectors_and_point(l1.vector,l1.vector.cross(l2.vector),l1.p1)
        return Point.from_plane_and_line(p,l2)

    @staticmethod
    def from_point_and_line(p,l):
        """ 
        l=a Segment
        p=a point
        returns the projection of p on  l
        """
        pl=AffinePlaneWithEquation(l.vector,p)
        return Point.from_plane_and_line(pl,l)

    
def is_vector(self):
    return isinstance(self,MassPoint) and (self[3]==0)

def is_point(self):
    return isinstance(self,MassPoint) and (self[3]==1)


class Base(list,Primitive):
    """
    class for basis in the massic space. This is a list of four vectors.

    Attributes:
    self[i], i in range(4) : the 4 mass points in the base 
    self.canToBase: The map sending the canonical basis to the vectors self[i]
    Base.canonical : the canonical base Base(X,Y,Z,T)=Base(X,Y,Z,origin)
    """

#    def __new__(cls,v0,v1,v2,v3):
#        return ()


    def __init__(self,v0,v1,v2,v3):
        super(Base,self).__init__([v0,v1,v2,v3])
        ObjectInWorld.__init__(self)
        self.canToBase=np.concatenate((v0,v1,v2,v3)).reshape(4,4).T.view(Map)
        #self.parts=[self[i] for i in range(4)]+[self.canToBase]

    def move_alone(self,M):
        self[:]=[M*i for i in self]
        self.canToBase=np.concatenate((self[0],self[1],self[2],self[3])).reshape(4,4).T.view(Map)



    def __str__(self):
        return  ("Base with matrix: \n"+np.ndarray.__str__(self.canToBase))

    def decompose_on(self,otherBase):
        inverse=np.linalg.inv(otherBase.canToBase)
        return(np.dot(inverse,self.canToBase).view(Map))

    @staticmethod
    def augmented(v0,v1,v2):
        """
        From a base of the vector space, computes a base of the massic space adding the origin
        """
        return Base(v0,v1,v2,point(0,0,0))



################################################################
"""
                Classes which inherit for Primitive
                They correspond to simple objects: plane, lines... 
"""
################################################################


class AffinePlane(Primitive):
    def __init__(self,*args,**kwargs):
        ObjectInWorld.__init__(self)


class AffinePlaneWithEquation(AffinePlane,np.ndarray):
    """ 
    An affine plane with equation ax_0+bx_1+cx_2+d=0.
    Equivalently, this is the equation  ax_0+bx_1+cx_2+dx_3=0 of a 3-dim linear space in the massic space.
    What is drawn in the 3D view is the half space  ax_0+bx_1+cx_2+d<=0, ie. the normal vector points outside the plane.


    Construction:
    p=AffinePlaneWithEquation(normal,markedPoint)
    p=AffinePlaneWithEquation(p1,p2,p3) 
    AffinePlaneWithEquation.from_bisector(p1,p2) : returns the bissector with normal p2-p1
    AffinePlaneWithEquation.from_bisector(segment) : as above with p1=segment.p1 and p2=segment.p2
    AffinePlaneWithEquation.from_coeffs(a,b,c,d):        Returns the plane ax+by+cz+d=0


    Attributes:
    normal: normal vector(a,b,c) pointing to the exterior (empty) half space.
    markedPoint : a point on the plane
    distanceFromOrigin is equal to the distance plane-Origin
    self[i,i in range(3)]=[a,b,c,d] the ndarray of coefficients.
    reverse(): replaces its normal by its opposite, thus inverts interior and exterior
    half_space_contains (point): returns true if the half space defined by the plane contains the point. True on the plane.
    """
    #  __functions__

    def __str__(self):
        return "Plane with equation "+" ".join([str(self[0]),"x+",str(self[1]),"y+",str(self[2]),"z+",str(self[3]),"=0"]) 

    def __new__(cls, *args,**kwargs):
        self=np.array(list((0.,0.,0.,0.))).view(cls)
        ObjectInWorld.__init__(self)
        #print(self.children)
        if len(args)==2:
            self.normal=args[0]
            self.markedPoint=args[1]
        elif len(args)==3:
            self.markedPoint=args[0]
            self.normal=(args[1]-args[0]).cross(args[2]-args[0])
        else:
            raise NameError('Wrong number of arguments in the function AffinePlaneWithEquation')
        self[0:4]=self.normal[0:4]
        self[3]=-self[0:3].dot(self.markedPoint[0:3])
        self.distanceFromOrigin=math.fabs(self.normal.dot(self.markedPoint-point(0,0,0))/self.normal.norm)
        return self



    def __init__(self,*args,**kwargs):
        pass

    def __array_finalize__(self,obj):
        try:
            myDict=obj.__dict__
        except:
            return
        for name in myDict:
            #print(name)
            attr=getattr(obj,name)
            setattr(self,name,attr)
            #pass
    @staticmethod
    def from_2_vectors_and_point(v1,v2,p):
        """
        returns the plane wiht normal v1.cross(v2) and passing through p
        """
        normal=v1.cross(v2)
        return AffinePlaneWithEquation(normal,p)
    @staticmethod
    def from_3_points(p1,p2,p3):
        return AffinePlaneWithEquation(p1,p2,p3)       
    @staticmethod
    def from_bisector(*args):
        """
        Constructor:
        AffinePlaneWithEquation.from_bisector(p1,p2) : returns the bissector with normal p2-p1
        AffinePlaneWithEquation.from_bisector(segment) : as above with p1=segment.p1 and p2=segment.p2
        """
        if len(args)==2:
            return AffinePlaneWithEquation(args[1]-args[0],0.5*args[0]+0.5*args[1])
        elif len(args)==1:
            segment=args[0]
            return AffinePlaneWithEquation(segment.p1-segment.p2,0.5*segment.p1+0.5*segment.p2)
        else:
            raise NameError('from Bisector takes one or two arguments')
    @staticmethod
    def from_2_points(p1,p2):
        """ returns the bisector plane"""
        return AffinePlaneWithEquation.from_bisector(p1,p2)
    @staticmethod
    def from_coeffs(a,b,c,d):
        """
        Returns the plane ax+by+cz+d=0
        """
        if not a==0:
            p=point(-1.*d/a,0,0)
        elif not b==0:
            p=point(0,-d*1./b,0)            
        elif not c==0:
            p=point(0,0,d*-1./c)
        else:
            raise NameError('The normal of a plane is a non zero vector')
        return AffinePlaneWithEquation(vector(a,b,c),p)
    @staticmethod
    def from_point_and_vector(p,v):
        return AffinePlaneWithEquation(v,p)
    @staticmethod
    def from_vector_and_point(v,p):
        return AffinePlaneWithEquation(v,p)


    
    #def copy(self):
        #myCopy=copy.deepcopy(self)
        #print("copie dans copy")
        # probably because of the inheritance from np.ndarray the attributes are not copied
        # so let's do this by hand. 
        #for name in self.__dict__:
            #print("Nom de l'attribut")
            #print(name)
            #setattr(myCopy,name,copy.deepcopy(getattr(self,name)))
        #return myCopy
    def __deepcopy__(self,memo):
        # I have to rewrite this because ndarray.deepcopy applies and forgets to copy the arguments
        cls = self.__class__
        result = np.ndarray.__deepcopy__(self,memo) 
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result
    def move_alone(self,M):
        #print("entree move-alone")
        #print("normal")
        #print(self)
        #print(self.normal)
        self.normal=M*self.normal
        #print(self)
        self[0:3]=self.normal[0:3]
        #print("affectation")
        #print(self)
        self.markedPoint=M*self.markedPoint
        self[3]=-self[0:3].dot(self.markedPoint[0:3])
        self.distanceFromOrigin=math.fabs(self.normal.dot(self.markedPoint-point(0,0,0))/self.normal.norm)
        #print("distance")
        #print(self)
        #print("Sortie")
        return self
    def reverse(self):
        #return self
        # modifies the plane so that the inside and outside are interverted.
        self.normal=-self.normal
        self[0:4]=-self[0:4]
        return self
    def evaluate_on(self,p):
        """
        returns the evaluation of the equation of the plane on p
        """
        return self.dot(p)
    def half_space_contains(self,point):
        if self.normal.dot(point-self.markedPoint)>0:
            return False
        else:
            return True
    def contains(self,point):
        if self.normal.dot(point-self.markedPoint)==0:
            return True
        else:
            return False
    def is_parallel_to(self,other_plane):
        if self.normal.cross(other_plane.normal).norm==0:
            return True
        else:
            return False
        

        
class ParametrizedCurve():
    """
    A class to factorize the methods common to all types of curves ( polyline,BezierCurve,PiecewiseCurve)

    """
    @staticmethod
    def from_function(f):
        myCurve=ParametrizedCurve()
        myCurve.__call__=f
        return myCurve

    
    @staticmethod
    def relativeToAbsolute(relativeList):
        #print("0",relativeList)
        if is_vector(relativeList[0]):
            relativeList[0]=origin+relativeList[0]
        else:
            relativeList[0]=relativeList[0]+0*X # not to share points between objects
                #print(relativeList[0])
                #print("changed 0")
        for i in range(1,len(relativeList)):
            if is_vector(relativeList[i]):
                #print(i,relativeList[i])
                #print(i-1,relativeList[i-1])
                relativeList[i]=relativeList[i]+relativeList[i-1]
                #print(relativeList[i])
                #print("changed")
            elif is_point(relativeList[i]):
                #print("not changed")
                relativeList[i]=relativeList[i].copy()
            else:
                raise NameError('relativeList['+str(i)+'] must be a point or vector')
        return relativeList
        
    def  reparametrize(curve,g):
        """
        Replaces the parametrize curve C(t) by C(g(t))  where g is a function corresponding to the change of parameter
        """
        oldCall=curve.__call__
        def composition(self,t):
            return oldCall(g(t))
        curve.__call__=types.MethodType(composition, curve)
        return curve

        
    def speed(curve,t,epsilon=0.00000001):
        """
        The speed vector at time t
        """
        if t>epsilon and t<1-epsilon:
            return (curve(t+epsilon)-curve(t-epsilon))/2/epsilon
        elif t>1-epsilon:
            return (curve(t)-curve(t-epsilon))/epsilon
        else:
            return (curve(t+epsilon)-curve(t))/epsilon

class FunctionCurve(ObjectInWorld,ParametrizedCurve):
    """ a class for curve defined by a function"""
    def __call__(self,t):
        return self.initialParametrizing(t)
    def __init__(self,f):
        #myCurve=ObjectInWorld.__new__(cls)
        #ObjectInWorld.__init__(self)
        self.initialParametrizing=f


    def move_alone(curve,M):
        oldCall=curve.__call__
        def composition(self,t):
            return M*oldCall(t)
        curve.__call__=types.MethodType(composition, curve)
        return curve

    def __deepcopy__(self,memo):
        myFunc=self.__call__
        theCopy=FunctionCurve(myFunc)
        memo[id(self)] = theCopy
        for k, v in self.__dict__.items():
            setattr(theCopy, k, copy.deepcopy(v, memo))
        return theCopy
        
        
class Polyline(list,Primitive,ParametrizedCurve):
    """ A class for polylines p0,...,pn ie the curve which is the union of segments p_i,p_{i+1}
    The sequence p_i is defined as a relative list, ie. the user may enter points or vectors and data are cast to the expected type as usual. 

    Constructors:
    Polyline(relativelist)
    relativelist: a list of points or vectors. 
 
    Methods: 
    self.lengths: [distance(p0,p1),distance(p1,p2)...]
    self.angles:[angle(p0,p1,p2),angle(p1,p2,p3),...,angle(p_{n-2},p_{n-1},p_n)]
    self.__call__(t): the parametrized point at time t. 
    self.show(): builds spheres along the curve for visualization
    """
    def  __call__(self,time):
        segmentDuration=1./(len(self)-1)
        leftPointIndex=int(floor(time*(len(self)-1)))
        #print(leftPointIndex)
        #print(self)
        if leftPointIndex==len(self)-1:
            return self[-1]
        timeLeftFromIndex=time-leftPointIndex*segmentDuration
        fractionOfSegment=timeLeftFromIndex*(len(self)-1)#=timeLef/segmentDuratio
        return (1-fractionOfSegment)*self[leftPointIndex]+fractionOfSegment*self[leftPointIndex+1]
    def __new__(cls,*args,**kwargs):
        return list.__new__(cls)
    def __init__(self,relativeList):
        self += ParametrizedCurve.relativeToAbsolute(relativeList)
        ObjectInWorld.__init__(self)
    def lengths(self):
        lengthsList=[]
        for i in range(len(self)-1):
            lengthsList.append((self[i+1]-self[i]).norm)
        return lengthsList
    def segments(self):
        segmentsList=[]
        for i in range(len(self)-1):
            segmentsList.append(Segment(self[i],self[i+1]))
        return segmentsList
    def angles(self):
        anglesList=[]
        for i in range(len(self)-2):
            anglesList.append(Triangle(self[i],self[i+1],self[i+2]).angle(1))
        return anglesList
    def __str__(self):
        return "Polyline  with control points "+", ".join([str(point) for point in self ])+"."
    def move_alone(self,M):
        [point.move_alone(M) for point in self ]
        return self
    def normal(self):
        """ assumes that the polyline is included in a plane to give the normal vector"""
        segments=self.segments()
        vector1=segments[0].vector
        vector2=segments[1].vector
        return vector1.cross(vector2).normalize()

class Polygon(Polyline):
    """ a polygon is a closed polyline included in a plane. In contrast to polylines, it is seen by the camera """
    pass
    
class BezierCurve(list,Primitive,ParametrizedCurve):
    """ A class for BezierCurve p0,...,pn ie this is the parametrized curve sum B^n_i(t) p_i with B^{n}_i(t)=(i choose n)(1-t)^i t^{n-i}
    In particular, this curve starts at p0 with tangent proportional to p1-p0 and ends at pn with tangent proportional to pn-p_{n-1} 
    The sequence p_i is defined as a relative list, ie. the user may enter points or vectors and data are cast to the expected type as usual. 

    Constructors:
    BezierCurve(relativelist)
    relativelist: a list of points or vectors. 
 
    Methods: 
    self.lengths: [distance(p0,p1),distance(p1,p2)...]
    self.angles:[angle(p0,p1,p2),angle(p1,p2,p3),...,angle(p_{n-2},p_{n-1},p_n)]
    self.__call__(t): the parametrized point at time t. 
    """
    def __new__(cls,*args,**kwargs):
        return list.__new__(cls)
    def __init__(self,relativeList):
        self += ParametrizedCurve.relativeToAbsolute(relativeList)
        ObjectInWorld.__init__(self)
    def lengths(self):
        lengthsList=[]
        for i in range(len(self)-1):
            lengthsList.append((self[i+1]-self[i]).norm)
        return lengthsList
    def angles(self):
        anglesList=[]
        for i in range(len(self)-2):
            anglesList.append(Triangle(self[i],self[i+1],self[i+2]).angle(1))
        return anglesList
    def __call__(self,time):
        output=0*Z
        for i in range(len(self)):
            output+=scipy.special.binom(len(self)-1, i)*((time)**i)*((1-time)**(len(self)-1-i))*self[i]
            #print i
            #print output
        return output
    def __str__(self):
        return "Bezier curve with control points "+", ".join([str(point) for point in self ])+"."
    def move_alone(self,M):
        [point.move_alone(M) for point in self ]
        return self
    #@staticmethod
    #def linear(*args):


class PiecewiseCurve(list,Primitive,ParametrizedCurve):
    """ 
    A class for piecewise curves C=[C0,\dots,Cn-1]. Ci is a polyline or Bezier curve, 
    and the end point of Ci is the initial point of C_{i+1} so that the curve is connected. 
    As a parametrized curve, the curve Ci  is described when the time is 
    in [i/n,(i+1)/n]. In other terms, the objects of the Curve class are curves 
    obtained by gluing together various curves which may be of different type. 

    Constructors:
    PiecewiseCurve(listOfCurves)
    listOfCurves: a list of polylines or bezier curvees
 
    Methods: 
    self.__call__(time): returns the point parametrized by time t. 
    """
    def __new__(cls,*args,**kwargs):
        return list.__new__(cls)
    def __init__(self,listOfCurves):
        ObjectInWorld.__init__(self)
        super(PiecewiseCurve,self).__init__(listOfCurves)
    def __str__(self):
        return "Compound curve with  the following curves:\n"+", \n".join([str(curve) for curve in self ])+"."
    def move_alone(self,M):
        [point.move_alone(M) for point in self ]
        return self
    @staticmethod
    def fromInterpolation(points,closedCurve=False):
        """ 
        parameters:
        points=list of points.
        This is an interpolated curve through the points p_0,\dots,p_n in argument. 
        The tangent at pi is parallel to p_{i+1}-p_{i-1}. 
        Technically, between pi and pi+1, 2 points qi and ri are inserted and 
        the curve number i in the compound is the Bezier Curve with points pi,qi,ri,pi+1. 
        For any i, the pair of points (p_i,p_{i+2}) should contain 2 distinct points otherwise 
        the tangent at p_{i+1}$ is not defined. 
        """
        if (len(points)<3):
            raise NameError('Need At least 3 points for the compound Curve')
        #print(points)
        ParametrizedCurve.relativeToAbsolute(points)
        #print(points)
        listeCurve=[]
        try:
            # first curve
            if not closedCurve:
                v0=(points[2]-points[0]).normalize()
                length=0.25*(points[1]-points[0]).norm
                q=points[1]-length*v0
                listeCurve.append(BezierCurve([points[0],q,q,points[1]]))
            else:
                v0=(points[1]-points[-2]).normalize()
                v1=(points[2]-points[0]).normalize()
                length=0.25*(points[1]-points[0]).norm
                q=points[0]+length*v0
                r=points[1]-length*v1
                listeCurve.append(BezierCurve([points[0],q,r,points[1]]))
            #intermediate curves 
            for i in range(len(points)-3):
                #print("log du milieu",i)
                #print("in fpl",[points[i],points[i+1],points[i+2],points[i+3]])
                v0=(points[i+2]-points[i]).normalize()
                v1=(points[i+3]-points[i+1]).normalize()
                length=0.25*(points[i+2]-points[i+1]).norm
                q=points[i+1]+length*v0
                r=points[i+2]-length*v1
                listeCurve.append(BezierCurve([points[i+1],q,r,points[i+2]]))
            # last curve
            if not closedCurve:
                v0=(points[-1]-points[-3]).normalize()
                length=0.25*(points[-1]-points[-2]).norm
                q=points[-2]+length*v0
                listeCurve.append(BezierCurve([points[-2],q,q,points[-1]]))
            else:
                v0=(points[-1]-points[-3]).normalize()
                v1=(points[1]-points[-2]).normalize()
                length=0.25*(points[-1]-points[-2]).norm
                q=points[-2]+length*v0
                r=points[-1]-length*v1
                listeCurve.append(BezierCurve([points[-2],q,r,points[-1]]))
        except:
            raise NameError('Error In Piecewise Curve.Maybe two points p_i,p_{i+2} are equal, in which case the tangent at p_{i+1} is not defined')
        return PiecewiseCurve(listeCurve)
    
    def  __call__(self,time):
        if (time>=1):# if >,probably because of floating numbers and should be 1
            #print("ici")
            return self[-1].__call__(1)
        else:
            #print(self)
            #print(floor(len(self)*time))
            curveNumber=int(floor(len(self)*time))
            timeInCurve=len(self)*time-curveNumber
            #print (curveNumber)
            #print (self[curveNumber])
            return self[curveNumber].__call__(timeInCurve)

        
class Circle(Primitive):
    """ 
    A class for circles defined by : a center, a radius, a plane

    Construction:
    p=Circle(center,radius,plane)
    p=Circle.from_2_points_and_tangent(p1,p2,v)


    Attributes:
    c.center
    c.radius: the radius a the time of creation
    c.plane
    """
    #  __functions__

    def __str__(self):
        return "Circle with center "+str(self.center)+ ", radius "+str(self.radius)+", in the plane "+str(self.plane)

    def __init__(self, center,radius,plane):
        ObjectInWorld.__init__(self)
        memo=dict()
        self.center=copy.deepcopy(center,memo).remove_children()
        self.radius=radius
        memo=dict()
        self.plane=copy.deepcopy(plane,memo).remove_children()

    def move_alone(self,M):
        if not M.is_orthogonal:
            raise NameError('A circle can be moved only by an orthogonal transformation')
        self.center=M*self.center
        self.plane=self.plane.move_alone(M)
        return self

    @staticmethod
    def from_2_points_and_tangent(p1,p2,v):
        """
        Constructor:
        p1, p2 : points in the circle, v: a vector tangent to the circle at p1
        """
        if not is_point(p1):
            print(p1)
            raise NameError('p1 not a point')
        if not is_point(p2):
            raise NameError('p2 not a point')
        if not is_vector(v):
            raise NameError('v not a vector')
            
        inThePlane=AffinePlaneWithEquation.from_3_points(p1,p2,p1+v)
        bisector=AffinePlaneWithEquation.from_bisector(p1,p2)
        plane2=AffinePlaneWithEquation(v,p1)
        center=Point.from_3_planes(inThePlane,bisector,plane2)
        radius=(p1-center).norm
        return Circle(center,radius,inThePlane)

    @staticmethod
    def from_tangent_triangle(triangle,radius):
        """
        Returns the circle of radius radius, tangent to the two lines of the triangles passing through point number 1.
        The circle comes with an attribute contact such that contact[0],contact[1] are the points of contact of the circle 
        with the lines Segment(p0,p1) and Segment(p1,p2).
        The contact points are children of the Circle and move with it. 
        """
        radius=float(radius)
        axis=Segment.from_bisector(triangle,i=1)
        angle=triangle.angle(1)
        center=axis.p1+radius/math.sin(angle/2)*((axis.p2-axis.p1).normalize())
        #print(radius*((axis.p2-axis.p1).normalize()))
        #print(center)
        contact=[]
        contact.append(Point.from_plane_and_line(AffinePlaneWithEquation(triangle[1]-triangle[0],center),Segment(triangle[1],triangle[0])))
        contact.append(Point.from_plane_and_line(AffinePlaneWithEquation(triangle[2]-triangle[1],center),Segment(triangle[1],triangle[2])))
        result=Circle(center,radius,triangle.plane())
        result.contact=contact
        contact[0].glued_on(result)
        contact[1].glued_on(result)
        return result

class Triangle(list,Primitive):
    """
    Constructor:
    Triangle(p0,p1,p2): pi= points

    Attributes:
    plane(): the plane containing the triangle: the marked point is p0. 
    angle(i): the unsigned angle at point pi, between 0 and pi
    angle_bisector(i): the bisector segment defined by angle at point pi. The two marked points of the line  are pi, and the point on the 
        bisector that lies on the opposite edge. 
    """

    def __str__(self):
        return "Triangle with points  "+" ".join([str(punct) for punct in self])

    def __init__(self,p0,p1,p2):    
        super(Triangle,self).__init__([p0,p1,p2])
        ObjectInWorld.__init__(self)

    def move_alone(self,M):
        [poi.move_alone(M) for poi in self]
        return self

    def angle(self,i):
        listCopy=copy.copy(self)
        base=listCopy.pop(i)
        vector1=(listCopy.pop()-base)
        vector1=vector1/vector1.norm
        vector2=(listCopy.pop()-base)
        vector2=vector2/vector2.norm
        return math.acos(vector1.dot(vector2))

    def angle_bisector(self,i):
        """
        The two marked points of the line  are the vertex of the angle, and the point on the 
        bisector that lies on the opposite edge. 
        """
        listCopy=copy.copy(self)
        base=listCopy.pop(i)
        point1=listCopy.pop()
        vector1=(point1-base)
        vector1=vector1/vector1.norm
        point2=listCopy.pop()
        vector2=(point2-base)
        vector2=vector2/vector2.norm
        axis1=Segment(base,0.5*vector1+0.5*vector2)
        axis2=Segment(point1,point2)
        return Segment(base,Point.from_2_lines(axis1,axis2))

    def plane(self):
        return AffinePlaneWithEquation.from_3_points(self[0],self[1],self[2])

class Polyhedral(AffinePlaneWithEquation):
    """
    Class for polyhedrals, aka intersection of half spaces
    
    Constructors 
    Polyhedral(listOfPlanes): the last item of the list is the father of the intersection
    """
    
    def __new__(cls,listOfPlanes):
        #print([plane.children for plane in listOfPlanes])
        myList=[ myPlane.copy() for myPlane in listOfPlanes ]
        #print([plane.children for plane in myList])
        poly=myList.pop()
        #print(poly.children)
        #print(myList)
        poly.intersected_by(myList)
        return poly


class AffineLine(Primitive):
    def __init__(self,*args,**kwargs):
        ObjectInWorld.__init__(self)
        

class AffineLineWithVectorDirector(AffineLine):
    pass
    #def base(self):
        

class Segment(AffineLineWithVectorDirector):
    """ 
    A class for segments [p1,p2] with p1 different from p2.
    Equivalently, this is marked oriented line,
    ie. lines + a point+a direction. The line goes through the segment,
    the point is the first point p1 and the vector=p2-p1.


    Atrributes:
    self.p1: the first point of the segment
    self.p2: the second point
    self.vector: the vector p2-p1

    Constructor:
    segment=Segment(start,end) where start=p1 and end=p2 or vector
    """
    def __init__(self,start,end):
        self.p1=start
        if is_vector(end):
            self.vector=end
            self.p2=self.p1+self.vector
        elif is_point(end):
            self.p2=end
            self.vector=self.p2-self.p1
        else:
            raise NameError('Wrong parameters for the Segment')
        if self.vector==vector(0,0,0):
            raise NameError('The vector p1-p2 is zero')
        ObjectInWorld.__init__(self)
        self.parts=[self.p1,self.p2,self.vector]

    def move_alone(self,M):
        #print("p1,M,M*p1",self.p1,M,M*self.p1)
        self.p1=M*self.p1
        self.p2=M*self.p2
        self.vector=self.p2-self.p1
        return self
    @staticmethod
    def from_point_and_vector(p,v):
        return Segment(p,v)
    @staticmethod
    def from_2_planes(p1,p2):
        myVector=p1.normal.cross(p2.normal)
        myPlane=AffinePlaneWithEquation(myVector,origin)
        myPoint=Point.from_3_planes(p1,p2,myPlane)
        return Segment(myPoint,myVector+myPoint)

    @staticmethod
    def from_bisector(triangle,i=1):
        #print("from bisect,i=",i)
        #print(triangle[2])
        return triangle.angle_bisector(i)

    def  point(self,x,coordinateType="p"):
        if coordinateType=="a":
            return self.p1+x*self.vector.normalized_copy()
        elif coordinateType=="p":
            return self.p1+x*self.vector
        elif coordinateType=="n":
            return self.p2-x*self.vector.normalized_copy()
        
    @property
    def norm(self):
        return self.vector.norm

    def __str__(self):
        return( "Line through"+str(self.p1)+" and "+str(self.p2)+" direction: "+str(self.vector))
    def prolonged_on_left(self,x):
        self.p1=self.p1-x*self.vector.normalized_copy()
        self.vector=self.p2-self.p1
        return self
    def prolonged_on_right(self,x):
        self.p1=self.p1-x*self.vector.normalized_copy()
        self.vector=self.p2-self.p1
        return self

class FrameBox(Base):
    """
    Class for quadruplets self.points[i], i in range(4) of points in the affine space.
    This quadruplet defines both a frame and a box, hence the name FrameBox.

    The frame is defined by 
    - three vectors self.vectors[i]=self.points[i+1]-self.points[0] for i in range(3).  
    - an origin  self.origin=self.points[0] 
    By definition a point p has coordinate c0,c1,c2 in this frame 
    if p=self.origin+\sum ci self.vectors[i]
    
    The box associated to the four points is by definition the smallest 
    parallelepiped containing the four points. In other words, the points 
    of the quadruplet are corner of the box, and the vectors of the frame 
    are edges of the box. 

    Attributes
    self.origin: the origin of the frame
    self.vectors : a 3-tuple containing the three vectors of the frame 
    self.points[i], i in range(4) : the 4 points of the frame
    self[i], in range(4) is the base of the massic space Base [self.vectors]+[self.origin]
    self.segments[i], i in range(3) : the segment Segment(self.origin,self.origin+self.vectors[i])
    self.dimensions = an alias for the 4-tuple  ( self.vectors[i].norm, i in range(3),dimOfTheDiagonal )
    self.point(x,y,z,frame="ppp") constructs a point whose coordinates are interpreted according to the frame string 
    self.face_center(faceVector=0*X) returns the center of a face in global coordinates.
    self.segment(x=None,y=None,z=None,frame="aa"): Returns a segment obtained by intersection of a line parallel to an edge with self.
    self.map_against(otherBox, selfFace1,otherFace1,selfFace2,otherFace2,offset=(0,0,0),
          adjustEdges=None,adjustAxis=None)  Returns a map to orientate self and translate it against otherBox. 
        

    Warning: the line from self.points[0] to self.points[i] is self.segments[i-1]. The same index shift
    occurs for vectors.

    Constructor
    framebox=Framebox(listOfPoints,xDirection=MassPoint(1,0,0,0),yDirection=MassPoint(0,1,0,0),zDirection=None,name="")
    builds  a FrameBox defined by the following conditions:
        - the box is the smallest box containing listOfPoints
        - the 3 vectors of the frame are positive multiples of xDirection,yDirection,zDirection
        - If zDirection is not filled, it is the cross product of xDirection and yDirection

"""
    def __init__(self,listOfPoints,xDirection=MassPoint(1,0,0,0),yDirection=MassPoint(0,1,0,0),zDirection=None,name=""):
        """
        Builds the a FrameBox defined by the following conditions:
        - the box is the smallest box containing listOfPoints
        - the 3 vectors of the frame are positive multiples of xDirection,yDirection,zDirection
        - If zDirection is not filled, it is the cross product of xDirection and yDirection
        """

        #print("xdri,ydir",xDirection,yDirection)
        if zDirection is None:
            zDirection=vector(np.cross(xDirection[0:3],yDirection[0:3]))
        #directions=[xDirection,yDirection,zDirection]
        M=Base.augmented(xDirection,yDirection,zDirection).canToBase
        Minv=np.linalg.inv(M)
        coordInBase=[Minv*i for i in listOfPoints]
        xmax=max(coord[0] for coord in coordInBase)
        xmin=min(coord[0]for coord in coordInBase)
        ymax=max(coord[1]for coord in coordInBase)
        ymin=min(coord[1]for coord in coordInBase)
        zmax=max(coord[2]for coord in coordInBase)
        zmin=min(coord[2]for coord in coordInBase)
        # Now the coordinates of the two extreme corners in the base xDirection,yDirection,zDirection
        mini=point(xmin,ymin,zmin)
        maxi=point(xmax,ymax,zmax)
        self.points=[]
        self.points.append(M*mini)
        self.points.append(self.points[0]+(maxi[0]-mini[0])*xDirection)
        self.points.append(self.points[0]+(maxi[1]-mini[1])*yDirection)
        self.points.append(self.points[0]+(maxi[2]-mini[2])*zDirection)
        self.origin=self.points[0]
        listeVecteursInit=[self.points[i+1]-self.points[0] for i in range(3)]
        super(FrameBox,self).__init__(*listeVecteursInit,v3=self.points[0])
        
        #self.parts=[self[i] for i in range(0,3)]+[self.points]+[self.canToBase]
        # Remark: self[3]=self.origin is a pointer to self.points[0], and self.origin is a pointer 
        # so there is no harm in considering only i<3 in move alone below. 
        # 

    def axis_permutation(self,i,j,k):
        """
        ij,k in 0,1,2
        permutes the  vectors X,Y,Z corresponding to indexes 0,1,2 and send them to i,j,k
        """
        M=Map.from_permutation(i,j,k)
        pointsCopy=copy.copy(self.points)
        #print("avt",self)
        self.points[1]=pointsCopy[i+1]
        self.points[2]=pointsCopy[j+1]
        self.points[3]=pointsCopy[k+1]
        self[0:3]=[self.points[i+1]-self.points[0] for i in range(3)]
        self.canToBase=self.canToBase*M
        return self

    def reverse_axis(self,i):
        """
        changes the vector i in 0,1,2 of the framebox to its opposite. The cube associated to the framebox is unchanged.
        """
        p=self.points[i+1].copy()
        vec=self[i]
        for j in range(4):
            self.points[j]+=vec
        #self.points[0]=p
        self.points[i+1]=p-vec
        listeVecteursInit=[self.points[i+1]-self.points[0] for i in range(3)]
        super(FrameBox,self).__init__(*listeVecteursInit,v3=self.points[0])
        return self
        
    def reorder(self):
        """reorder the points of the frame so that the local coordinate of the frame corresponds 
        to the global coordinate of the world (at the linear level,not affine level). In other words, 
        the first vector is (close to) parallel to X (resp. second,third to Y,Z)
        useful when the box has been moved and we want to permute the axes for clarity 
        """
        perm=[]
        for i in range(3):
            #print("le self")
            #print (self[i])
            #max_value = max(self[i])
            selfabs=[math.fabs(self[i][j]) for j in range(4)]
            perm.append(np.argmax(selfabs))
        #print("permutation",perm)
        permInverse=[]
        for i in range(3):
            permInverse.append(perm.index(i))
        #print("pinverse",permInverse)
        self.axis_permutation(*permInverse)
        # now the lines through the axis are correct, but maybe the orientation of the vectors is not correct.
        # the following lines deal with the orientation
        for i in range(3):
            if self[i][i]<0:
                self.reverse_axis(i)
        return self
    
    def move_alone(self,M):
        self.points=[i.move_alone(M) for i in self.points]
        self[0:3]=[self.points[i+1]-self.points[0] for i in range(3)]
        self.canToBase=M*self.canToBase
        return self

    @property
    def vectors(self):
        return tuple([self.points[i+1]-self.points[0] for i in range(3)])

    @property
    def dimensions(self):
        # returns [dimx,dimy,dimz,dimOfTheDiagonal]
        a=[(self.points[i+1]-self.points[0]).norm for i in range(3)]
        b=vector(*a).norm
        a.append(b)
        return tuple(a)


    def __str__(self):
        string="FrameBox:\n"
        string+="Origin: "+str(self[3])+"\nVectors:\n"
        for i in range(3):
            string+=str(self[i])+ " \n"
        return (string)

    def _to_proportional_coordinate(self,coord,letter,dim):
        """
        cast a coordinate given in any form (absolute, negative or proporitional) to a coordinate
        in the proportional frame
        """
        if letter=="n":
            return((dim-coord)/dim)
        if letter=="a":
            return (coord/dim)
        if letter=="p":
            return(coord)
        raise NameError("The letter in prop coord should be in 'anp', not"+str(letter))

    def _from_proportional_coordinate(self,coord,letter,dim):
        """
        cast a coordinate given  the local proportional frame
        to a coordinate in any local form (absolute, negative or proporitional)
        """
        if letter=="n":
            return (dim-coord*dim)
        if letter=="a":
            return (coord*dim)
        if letter=="p":
            return(coord)
        raise NameError("The letter in prop coord should be in 'anp', not"+str(letter))

    def point(self,x=0,y=0,z=0,frame="ppp"):
        """
        Returns a point computed from local coordinates x,y,z in the frame.
        The parameter "frame" describes the convention for local coordinates:
        a for absolute, n for negative absolute and p using percents. 
        """
        input=[x,y,z]
        codeFrame=list(frame)
        frameCoordinates=vector(*[self._to_proportional_coordinate(
            input[i],codeFrame[i],self.dimensions[i]) for i in range(3)])
        #print(frameCoordinates)
        globalCoordinates=self.canToBase*frameCoordinates+self.points[0]
        return globalCoordinates

    def _face_vector_to_couple(self,vector):
        """
        returns the couple (index,sign) where index is the index of the non vanishing coordinate
        of vector and sign is the corresponding sign
        Useful to get the coordinate and the direction of a face given as a Vector
        """
        vectorAbs=[math.fabs(vector[j]) for j in range(3)]
        index=vectorAbs.index(max(vectorAbs))
        sign=copysign(1,vector[index])
        #print("in _fv2c")
        #print([sign])
        return([index,sign])

    def _face_couple_to_vector(self,index,sign):
        """
        A face is described with a number. The center of this face in proportional coordinates 
        is returned. This is the inverse function of _face_vector_to_couple.
        """
        w=vector(0,0,0)
        w[index]=sign
        return (w)

    def face_center(self,faceVector=MassPoint(0,0,0,0)):
        """
        returns the center of a face in global coordinates.
        This can be a 0 dim face (example: faceVector=(X-Y-Z)) 1 dim (ex: faceVector=-X+Z)
        2 dim ( fV=X) or 3 dim (fV left to default )
        """
        localCoord=vector(0.5,0.5,0.5)+0.5*faceVector
        return ( self.point(*localCoord[0:3],frame="ppp"))

    def _parallel_face(self,faceAsVector,otherBox):        
        """
        This function assumes that self and otherBox are parallel boxes.
        Takes a face of self in input (ie in the form +-X,+-Y...)
        and returns the face of OtherBox parallel to it (as a vector too)
        """
        normal=self._face_information(faceAsVector).normal
        tableau=[normal.dot( otherBox[j] ) for j in range(3)]
        #print("tableau",tableau)
        tableauAbs=[math.fabs(normal.dot( otherBox[j])) for j in range(3)]
        #print("tableauAbs",tableauAbs)
        index=tableauAbs.index(max(tableauAbs))
        sign=tableau[index]/tableauAbs[index]
        v=vector(0,0,0)
        v[index]=sign
        #print(v)
        return(v)


    def segment(self,x=None,y=None,z=None,frame="aa"):
        """
        Returns a segment obtained by intersection of a line parallel to an edge with self.
        For instance, an input x=2,y=None,z=3 means that 
        y is the axis of the line and x are z are the coordinates of the line in a face 
        orthogonal to the axis y. The coordinates of x,z are interpreted as absolute,negative or 
        proportional depending on the parameter frame. By default, frame="aa" meaning both
        coordinates are absolute.
        """
        local=[x,y,z]
        dimSelf=self.dimensions[0:3]
        localCoordinates=[]
        globalCoordinates=[]
        for k in range(2): # we build 2 points globalCoordinates[k] for the segment
            codeFrame=list(frame)
            localCoordinates.append([])
            globalCoordinates.append([])
            for i in range(3):
                if local[i] is not None:
                    localCoordinates[k].append(self._to_proportional_coordinate(local[i],codeFrame[i],dimSelf[i]))
                else :
                    localCoordinates[k].append(k)
                    codeFrame=[""]+codeFrame
            globalCoordinates[k]=self.point(localCoordinates[k][0],localCoordinates[k][1],localCoordinates[k][2],"ppp")
        return Segment(globalCoordinates[0],globalCoordinates[1])


    def plane(self,face,coord,frame="a"):
        """
        Returns the plane parallel to face, containing the point whose coordinate on the transversal line is coord. 
        """
        # Among x,y,z below, one of them is coord, and two of them vanish, ie we affect coord to the adequate axis.
        x=coord*(fabs(face[0]))
        y=coord*(fabs(face[1]))
        z=coord*(fabs(face[2]))
        p=self.point(x,y,z,frame=frame+frame+frame)
        return AffinePlaneWithEquation(self._face_information(face).normal,p)

    def _face_information(self,vector):
        """
        returns the faceInformation of the box, its center, normal....
        """
        center=self.face_center(vector)
        normal=0.5*(center-self.face_center(-vector))#towards the outside
        dimension=3-sum(vector)
        myFace=FaceInformation(center,normal,dimension)
        return myFace

    def _map_for_parallelism(self,otherBox,selfFace1,otherFace1,selfFace2,otherFace2):
        """
        returns a map M such that M(self) is a box whose faces selfFace1,selfFace2 are 
        parallel to the faces otherFace1 and otherFace2 of otherBox if this is possible.
        When it's not possible because the angles are not the same, then
        M(selfFace1) is parallel to otherFace1 and the plane selfFace1,selfFace2 coincides
        with the plane otherFace1.otherFace2. The faces are described 
        using a vector v in [X,-X,...Z,-Z]. The parallelism in the above description takes into 
        account the sign of v, ie by parallel we mean that the normal of the faces
        are positivly proportional. 
        """
        s1=self._face_information(selfFace1).normal
        s2=self._face_information(selfFace2).normal
        s3=s1.cross(s2)
        o1=otherBox._face_information(otherFace1).normal
        o2=otherBox._face_information(otherFace2).normal
        o3=o1.cross(o2)
        S=Base.augmented(s1,s2,s3)
        O=Base.augmented(o1,o2,o3)
        qs, rs = np.linalg.qr(S.canToBase)
        qo, ro = np.linalg.qr(O.canToBase)
        # I change the signs of qs qo because they don't respect the orientation of the frame
        qs = np.ndarray.__mul__(qs,np.sign(np.diag(rs)))
        qo = np.ndarray.__mul__(qo,np.sign(np.diag(ro)))
        return qo*np.linalg.inv(qs)


    def _map_translate_against(self,otherBox, faceOfSelf=None, offset=(0,0,0),adjustEdges=None,adjustAxis=None):
        """
        returns a translation M useful to move a box against an other box,
        This means that ( if the offset parameter is unchanged), M(self) and otherBox have 
        a face contained in a common plane.  The face of self automatically determines the corresponding
        face of other Box. For instance, if self and otherBox are parallel to the canonical frame, and if 
        one uses the top face of self, one has to use the bottom face of OtherBox to move self
        against otherBox.

        This function makes sense if the boxes
        are parallel. If not, the function tries to compute pairs of parallel faces and returns
        a matrix of translation such that the centers of the faces coincide. But the significance of the orientation
        of the box is not guaranteed if the boxes are far from being parallel.

        By default, the associated faces G of M(self) and F of otherBox share  
        the same center. This default may be changed using the offset parameter.
        If offset is a tuple of float or a vector, then centerG=centerF+offset.

        An other possible variation from the default is to replace the common center of the faces
        by a common edge or a common corner. Suppose for instance that the face of self 
        we are considering is Y.
        Then this face of self  admits two local coordinates x,z. In this
        face,there are 4 edges, denoted by X,-X,Z,-Z, and 4 corners that we denote by
        X+Z,X-Z,-X+Z,-X-Z. If the parameter adjustEdges is set to adjustEdges=-X, then M(self)
        is such that the edge -X of self is moved along the corresponding edge of otherBox,
        ie. there is a common line containing the two edges and the two edges have
        the same center. It adjustEdges=X-Z then M(self) is such that the corner X-Z of self
        coincides with a corner of otherBox.

        A final option to adjust the placement is given by the parameter
        adjustAxis=[markerOfSelf,markerOfOtherBox]. Comparing to the default, 
        self is translated by keeping the plane of contact between the faces. 
        The map M is such that 
        M(markerOfSelf) and markerOfOtherBox are aligned on an axis orthogonal 
        to the common plane. The markers may be a point
        or a line transversal to the common plane.

        If the three parameters adjustEdges, offset and adjustAxis
        are changed from their default value, then all of them 
        are used: M first adjusts theAxis, then moves using adjustEdges, then the offset is added.
        In other words, the total shift is the sum of each of the three shifts. 
        """
        


        # First, we translate to make the centers coincide
        #print("parallelFace")
        #print(self._parallel_face(faceAsVector=faceOfSelf,otherBox=otherBox))
        vectorOtherFace=-self._parallel_face(faceAsVector=faceOfSelf,otherBox=otherBox)
        #print("vectorOtherFace")
        #print(vectorOtherFace)
        #print("faceOfSelf")
        #print(faceOfSelf)
        vTranslation=otherBox.face_center(vectorOtherFace)-self.face_center(faceOfSelf)
        #print("vtrans1",vTranslation)
        #print(faceOfSelf)
        #print(self)
        #print(self.face_center(faceOfSelf))
        #print(self.point(0,0.5,0.5,"ppp"))
        #print(otherBox.face_center(vectorOtherFace))
        #print(vectorOtherFace)
        #print(otherBox)
        #print(vTranslation)
        # Now, we adjust along the axis
        if adjustAxis is not None:
            # We extract the required information point1 and point 2 from the markers. These points are
            # the markers adjustAxis[i] themselves or a point on the line if one of the marker is a line
            if isinstance(adjustAxis[0],AffineLine):
                point1=adjustAxis[0].p1
            else:
                point1=adjustAxis[0]
            if isinstance(adjustAxis[1],AffineLine):
                point2=adjustAxis[1].p1
            else:
                point2=adjustAxis[1]
            # We project the markers point1 and point2 to the common plane. This is done with the vanishing
            # of the appropriate coordinate in local coordinate, then turning back to global coordinate.
            # The translation vector is the difference between these two projections.
            #print(self.canToBase)
            pointLocal1=self.canToBase*(point1+vTranslation)
            pointLocal2=self.canToBase*point2
            coordinateNumber=self._face_vector_to_couple(faceOfSelf)[0]
            pointLocal1[coordinateNumber]=0
            pointLocal2[coordinateNumber]=0
            M=self.canToBase.inverse()
            vTranslation=vTranslation+M*pointLocal2-M*pointLocal1
            #vTranslation=M*pointLocal2-M*pointLocal1


        # We push along edges if necessary.

        if adjustEdges is not None:
            #  First,we compute correspondanceDirections(i)=(j,sign) such that the
            # the face  (i,+1) of self is parallel to face (j,sign) of otherBox
            correspondanceDirections={}
            for i in range(3):
                faceAsVector=self._face_couple_to_vector(i,1)
                #print(otherBox._face_vector_to_couple(self._parallel_face(faceAsVector=faceAsVector,otherBox=otherBox)))
                correspondanceDirections[i]=otherBox._face_vector_to_couple(
                    self._parallel_face(faceAsVector=faceAsVector,otherBox=otherBox))
            #print(correspondanceDirections)
            #deltaDim=vector([-self.dimensions[i]+otherBox.dimensions[correspondanceDirections[i][0]] for i in range(3)])
            deltaDim=vector([-1+(otherBox.dimensions[correspondanceDirections[i][0]])/self.dimensions[i] for i in range(3)])
            #print("deltaDim",deltaDim)
            #print("adjustEdges",adjustEdges)
            vAlignLocal=vector([deltaDim[i]*adjustEdges[i]/2 for i in range(3)])
            #vAlignGlob
            #print(vAlignLocal)
            #print(self.canToBase*vAlignLocal)
            #print(self.canToBase)
            vAlignGlobal=self.canToBase*vAlignLocal
            vTranslation=vTranslation+vAlignGlobal

        from aliases import is_vector

        #Now we add the offset
        if isinstance(offset,tuple):
            vOffset=vector(offset)
        elif is_vector(offset):
            vOffset=offset
        else:
            raise NameError('Offset should be a tuple or a vector')
        vTranslation=vTranslation+vOffset
        return Map.translation(vTranslation)


    # seems buggy: if needed, see the function with the same name for objects, where the bugs have been corrected.
    # def map_against(self,otherBox, selfFace1,otherFace1,selfFace2,otherFace2,offset=(0,0,0),adjustEdges=None,adjustAxis=None):
    #     """
    #     Returns a map to orientate self and translate it against otherBox. The face of contact between the two boxes is the face selfFace1.
    #     For further doc, look _map_for_parallelism and _map_translate_against as this function is just a wrapper. 
    #     """
    #     M=self._map_for_parallelism(otherBox,selfFace1,otherFace1,selfFace2,otherFace2)
    #     N=self.copy().move(M)._map_translate_against(otherBox, faceOfSelf=selfFace1, offset=offset,adjustEdges=adjustEdges,adjustAxis=adjustAxis)
    #     return(N*M)
    @staticmethod
    def from_union(liste):
        """ 
        elements in the list are frameboxes or objects with a box. Returns the union of boxes
        """ 
        newlist=[]
        for entry in liste:
            if not isinstance(entry,FrameBox):
                entry=entry.box()
                newlist.append(entry.point(0,0,0,"ppp"))
                newlist.append(entry.point(1,1,1,"ppp"))
        return FrameBox(newlist)
        

class FaceInformation(object):
    """
    The faceInformation of a frameBox
    """
    def __init__(self,center,normal,dimension):
        self.center=center
        self.normal=normal
        self.dimension=dimension

    def __str__(self):
        string= "Face of dimension "+str(self.dimension)+", with center "+str(self.center)+", and outer normal"+str(self.normal)
        return string



################################################################
"""
                Maps in the massic space, aka massic maps
                The explicit maps rotation, translation
                and map operations (inverse..) are
                attributes of this class

"""
################################################################

class Map(np.ndarray):
    """
    Class for massic maps. In this space the affine maps, identified with massic maps 
    with matrices whose last line is [0,0,0,1]. The linear maps are identified with affine maps
    fixing (0001). With this formalism, the linear part of an affine map.
    is obtained by replacing the last column with (0001). 
    In particular, evaluation on massic points and on vectors makes sense.
    The product M*O is a point,a vector,a map when O is a point,a vector,a map. 

    Warning:  this formalism is not compatible with the vector space structure of linear maps. 

    Attributes
    self.inverse(): computes the inverse map
    Map.linear(v0,v1,v2) : the linear map sending Base.canonical to (v0,v1,v2,origin)
    Map.affine(v0,v1,v2,w): the linear map followed by a translation of vector w.
    Map.translation(x,y,z)=Map.translation(vector(x,y,z))
    Map.rotation(axis,angle), axis=the affine oriented line axis of the rotation. The angle is positive if the rotation screws towards the oriented axis.
    Map.scale(fx=1,fy=1,fz=1,xVector=X,  yVector=Y, zVector=Z,fixedPoint=origin):
    Map.from_base_to_base(self,base1,base2) : Returns a map sending base1 to base2. 
    Map.rotational_difference(start=None,end=None), start, and end: 2 vectors
    Map.identity
    """

    def __new__(cls,v0,v1,v2,w):
        """
        The linear map sends the canonical base to vo,v1,v2, followed by translation
        of vector w
        """
        return( np.concatenate((v0,v1,v2,w)).reshape(4,4).T.view(cls))

    def __init__(self,*args):
        pass


    def __mul__(self,other):
        """
        returns the composition or the evaluation with other, depending on the type of other
        """
        if isinstance(other, MassPoint ):
            result=self.dot(other).view(MassPoint)
            ObjectInWorld.__init__(result)
            return result
        elif  isinstance(other, Map ):
            return( self.dot(other))
        else:
            raise NameError('Unsupported product for Massic Map and'+str(type(other)))
            
    def inverse(self):
        return np.linalg.inv(self).view(Map)


    def is_orthogonal(self):
        # returns true is self is orthogonal as a float matrix. 
        return np.allclose((self)[0:3,0:3].dot(np.transpose(self)[0:3,0:3]),(Map.identity)[0:3,0:3])

    @staticmethod
    def linear(v0,v1,v2):
        """
        The linear map which sends the canonical base to vo,v1,v2
        """
        return( Map(v0,v1,v2,MassPoint(0,0,0,1)))

    @staticmethod
    def affine(v0,v1,v2,w):
        """
        The affine map which sends the canonical base to vo,v1,v2 and translation w
        """
        translationVector=w.copy()
        translationVector[3]=1
        return( Map(v0,v1,v2,translationVector))



    @staticmethod
    def translation(*args):
        """
        The input arguments are either
        - a triplet for the coordinates of the vector
        - a vector
        """
        if len(args)==1:
            w=args[0].copy()
        else:
            w=vector(*args)
        w[3]=1
        return(Map.affine(X,Y,Z,w))

    @staticmethod
    def rotation(axis,angle):
        """
        Return the rotation matrix associated with rotation about
        the given axis by angle radians. If  the angle is positive,
        a screw following the rotation goes towards the axis direction
        (aka right handed convention).
        THis default can be changed with the variable screwPositiveRotations
        """
                
        if screwPositiveRotations :
            angle=-1*angle
        if isinstance(axis,AffineLine):
            myVector = np.asarray(axis.vector)
            N=Map.translation(axis.p1).view(Map)
        elif is_vector(axis):
            myVector = axis
            N=Map.translation(T).view(Map)
        else:
            raise NameError('Error of type for axis is:'+str(type(axis)))
        angle = np.asarray(angle)
        myVector = myVector/math.sqrt(np.dot(myVector, myVector))
        a = math.cos(angle/2)
        b, c, d , e = myVector*math.sin(angle/2)
        aa, bb, cc, dd = a*a, b*b, c*c, d*d
        bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
        return N*np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac), 0],
                         [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab), 0],
                         [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc, 0],
                         [0        , 0        , 0           ,1]]).view(Map)*np.linalg.inv(N).view(Map)

    @staticmethod
    def linear_rotation(vectorAxis,angle):
        return Map.rotation(axis=Segment(origin,origin+vectorAxis),angle=angle)

    @staticmethod
    def scale(fx=1,fy=1,fz=1,xVector=MassPoint(1,0,0,0),  yVector=MassPoint(0,1,0,0), zVector=MassPoint(0,0,1,0),fixedPoint=MassPoint(0,0,0,1)):
        """
        """
        base1=Base.canonical
        base2=Base(xVector,yVector,zVector,fixedPoint)
        v0=vector(fx,0,0)
        v1=vector(0,fy,0)
        v2=vector(0,0,fz)
        M=Map.linear(v0,v1,v2)
        return (M.from_base_to_base(base1,base2))

    @staticmethod
    def rotational_difference(start=None,end=None,point1=None,point2=None):
        """
        start=vector
        end=vector
        returns an affine map M. The linear part is the rotation sending the vector start to a positive multiple of the vector end.
        The axis of the rotation is given by the cross product of start with end, and it
        is chosen randomly when start and none are proportional. If point1 and point2 are not none, M(point1)=point(2), otherwise M(origin)=origin
        """
        vector1=start[0:4]
        vector2=end[0:4]
        rotationVector=vector1.cross(vector2)
        if rotationVector.is_origin():
            # the two vectors are proportional, angle is zero or pi, I choose a random orthogonal vector for the axis
            minIndex=np.argmin(vector1*vector1)
            #print(vector1*vector1)
            #print("minIndex",minIndex)
            rotationVector[minIndex]=1
            #print(rotationVector)
            #print(vector1)
            rotationVector=vector1.cross(rotationVector)
            #print(rotationVector)
        #print(rotationVector)
        axis=Segment(point(0,0,0),rotationVector)
        cosine= np.dot(vector2,vector1)/np.linalg.norm(vector1)/np.linalg.norm(vector2) # -> cosine of the angle
        angle = np.arccos(np.clip(cosine, -1, 1))
        if not screwPositiveRotations:
            angle=-angle
        M=Map.rotation(axis,angle)
        if point1 is not None and point2 is not None:
            #print("not None")
            vecteur=point2-M*point1
        else:
            vecteur=vector(0,0,0)
        return Map.affine(M*X,M*Y,M*Z,vecteur)


    def from_base_to_base(self,base1,base2):
        """
        This method moves a map from base1 to base2, ie. if R is the map returned matrix(R,base2)=matrix(self,base1)
        """
        M=base2.decompose_on(base1)
        return (M*self*np.linalg.inv(M).view(Map))
    
    @staticmethod
    def from_permutation(a,b,c):
        def _to_vector(i):
            if i==0: return vector(1,0,0)
            if i==1: return vector(0,1,0)
            if i==2: return vector(0,0,1)
            raise NameError("i should be 0,1 or 2")
        M=Map.linear(_to_vector(a),_to_vector(b),_to_vector(c))
        return M

    @staticmethod
    def flipXY():
        return Map.linear(Y,X,Z)
    @staticmethod
    def flipXZ():
        return Map.linear(Z,Y,X)
    @staticmethod
    def flipYZ():
        return Map.linear(X,Z,Y)
    @staticmethod
    def flipX():
        return Map.linear(-X,Y,Z)
    @staticmethod
    def flipY():
        return Map.linear(X,-Y,Z)
    @staticmethod
    def flipZ():
        return Map.linear(X,Y,-Z)
    
class Rotation(Map):
    """ 
    A class  to generate rotations
    """
    @staticmethod
    def from_axis_and_target_points(l,p1,p2):
        """
        returns a rotation R with axis l such that R(p1),R(p2),l.p1,l.p2 are coplanar in some plane P and 
        R(p1) and R(p2) are in the same half plane of the punctured plane P-l
        """
        vector1=(p1-p1.projection_on_line(l)).normalize()
        vector2=(p2-p2.projection_on_line(l)).normalize()
        #print("les vecteurs",vector1,vector2)
        cosangle=vector1.dot(vector2)
        if  (vector1.cross(vector2)).dot(l.vector) >0:
            angle=math.acos(cosangle)
        else: angle=-math.acos(np.clip(cosangle, -1, 1))
        #print("angle",angle/math.pi)
        if not screwPositiveRotations:
            angle=-angle
        #print(angle)
        #print("verif Rotation.from_axis","1 et 2 prop",p2,Map.rotation(l,angle)*p1)
        #print("verif Rotation.from_axis","1 et 2 prop",vector2,Map.rotation(l,-angle)*vector1)
        return Map.rotation(l,angle)


def _screw_map(self,other,adjustAlong=None,adjustAround=None):
    """ 
    self=a Segment
    other=a Segment
    adjustAlong=[point1,point2]
    adjustAround=[point3,point4]
    Retruns an isometry map M such that 
    - M(self).vector et otherAxis.vector are positivly proportional
    - M(self) et otherAxis have a point in common
    - M(point1)-point2 is orthogonal to otherAxis.vector
    -M(point3),point4 is a line coplanar to otherAxis and in the same half plane
    """
    M=Map.rotational_difference(self.vector,other.vector,self.p1,other.p1)
    if adjustAlong is not None:
        myVector=adjustAlong[1].projection_on_line(other)-(M*adjustAlong[0]).projection_on_line(other)
        M=Map.translation(myVector)*M
    if adjustAround is not None:
        M=Rotation.from_axis_and_target_points(other,M*adjustAround[0],adjustAround[1])*M
    return M

Segment.screw_map=_screw_map
    
################
"""
    global math objects
"""
################

def vector(*args):
    """
    The input arguments are 
    a triplet for the coordinates of the vector
    or an np.array
    """
    if len(args)==3:
        return MassPoint(args[0],args[1],args[2],0)
    elif len(args)==1:
        return MassPoint(args[0][0],args[0][1],args[0][2],0)

def point(x,y,z):
    return (MassPoint(x,y,z,1))


X=vector(1,0,0)
# Object In world is modified later, so I need to introduce children by hand
X.children=[]
Y=vector(0,1,0)
Y.children=[]
Z=vector(0,0,1)
Z.children=[]
T=point(0,0,0)
T.children=[]
origin=T
    



Base.canonical=Base(X,Y,Z,T)
Map.identity=Map.affine(X,Y,Z,T)


