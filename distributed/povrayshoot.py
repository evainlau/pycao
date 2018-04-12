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


import os 
import sys
sys.path.append(os.getcwd()) # pour une raison inconnue, le path de python ne contient pas ce dir dans l'install de la fac

from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *


def povrayVector(p):
    return("<"+str(p[0])+","+str(p[1])+","+str(p[2])+">")

def point_to_povray2d(p,i,j):
    " casts a vector v to the string '<v[i],v[j]>'"
    return("<"+str(p[i])+","+str(p[j])+">")

def povrayMatrix(M):
    string="<"
    for j in range(4):
        for i in range(3):
            string=string+str(M[i][j])
            if i<2 or j<3:
                string=string+" , "
    string=string+">"
    return(string)



def color_string(self):
    if self.color is None:
        return ""
    else:
        string="pigment {color "+self.color+"}"
        return string


def modifier_texture(self,camera):
    "Returns a string describing the texture of the object"
    string=""
    if self.visibility<camera.visibilityLevel:
        string+=" no_shadow no_image no_reflection \n" 
    try:
        string+=self.material+"\n"
    except AttributeError:
        if  self.color is not None:
            string+=" material{texture{ "+ color_string(self)+ " finish{metallic phong 1} }} \n "
    return string

def modifier_matrix(self):
    "Returns a string describing the matrix self.mapFromParts of the object"
    if isinstance(self,Primitive):
        string= ""
    else:
        string="matrix "+povrayMatrix(self.mapFromParts)
    #return ""
    return string



def modifier(self,camera):
    "Returns a string describing the modifier of the object"
    return modifier_texture(self,camera)+modifier_matrix(self)




def object_string_but_CSG(self,camera):
    """
    This is the code to get the string for an object which has no csg operations. 
    """
    try:
        string="\n//name: "+self.name+"\n"
    except AttributeError:
        string="\n//Unnamed Object\n"
    if isinstance(self,Cylinder) or isinstance(self,Cone):
        if self.parts.open:
            openString=" open "
        else:
            openString=""
    if isinstance(self,Cylinder):
        string+="cylinder{"+povrayVector(self.parts.start)+","+povrayVector(self.parts.end)+","+str(self.parts.radius)+ openString+" "+modifier(self,camera)+"}"
    if isinstance(self,ICylinder):
        string+="quadric{"+povrayVector(vector(1,1,0))+","+povrayVector(vector(0,0,0))+"," +povrayVector(vector(0,0,0)) + ",-"+str(self.parts.radius**2)+ modifier(self,camera)+"}"
    elif isinstance(self,Torus) :
        string+="torus {\n"+str(self.parts.externalRadius)+","+str(self.parts.internalRadius)+" "+modifier(self,camera)+"}\n"
    elif isinstance(self,Cube) :
        string+="box {\n"+povrayVector(self.parts.start)+","+povrayVector(self.parts.end)+" "+modifier(self,camera)+"}\n"
    elif isinstance(self,Sphere) :
        string+="sphere {\n"+povrayVector(self.parts.center)+","+str(self.parts.radius)+" "+modifier(self,camera)+"}\n"
    elif isinstance(self,AffinePlane) :
        string+="plane {\n"+povrayVector(self.normal)+","+str(-self[3]/self.normal.norm)+" "+modifier(self,camera)+"}\n"
        # Orientation Checked with the following code
        #s=Sphere(origin,.1).colored("Red")
        #p1=plane(Z,origin+.05*Z)
        #p1=plane(Z,origin-.05*Z)
        #p1=plane(-Z,origin+.05*Z)
        #p1=plane(-Z,origin-.05*Z)
        #s.intersected_by(p1)
    elif isinstance(self,Cone) :
        #print(self)
        string+="cone {\n"+povrayVector(self.parts.start)+","+str(self.parts.radius1)+"\n"+ povrayVector(self.parts.end)+","+str(self.parts.radius2)+" "+modifier(self,camera)+"}\n"
    elif isinstance(self,Lathe) :
        if isinstance(self.parts.curve,Polyline):
            latheType="linear_spline"
        elif isinstance(self.parts.curve,BezierCurve):
            latheType="bezier_spline"
        string+="lathe {\n"+latheType+" "+str(len(self.parts.curve))+"\n"
        for p in self.parts.curve: string+=","+point_to_povray2d(p,1,2)
        string+=modifier(self,camera)+"}\n"
    elif isinstance(self,RuledSurface):
        string+="mesh2 { vertex_vectors { "+str(2*len(self.parts.timeList1))+"\n"
        for t in self.parts.timeList1:
            string+=","+povrayVector(self.parts.curve1.__call__(t))
        string+="\n"
        for t in self.parts.timeList2:
            string+=","+povrayVector(self.parts.curve2.__call__(t))
            #print self.parts.curve1.__call__(t)
        string+=" }\n   normal_vectors { "+str(2*len(self.parts.timeList1))
        for i in xrange(len(self.parts.timeList1) - 1):
            xi,xip = self.parts.curve1.__call__(self.parts.timeList1[i]), self.parts.curve1.__call__(self.parts.timeList1[i + 1])
            yi=self.parts.curve2.__call__(self.parts.timeList2[i])
            #print("xi,yi,xip...",xi,yi,xip,xi-yi,xip-xi)
            #normal=(xi-yi).cross((xip-xi))
            normal=(xi-yi).cross((self.parts.curve1.speed(self.parts.timeList1[i])))
            #print(normal,"normal")
            #print(normal.normalized_copy())
            #print(normal.normalized_copy())
            string+=","+povrayVector(normal)
            if i==len(self.parts.timeList1) - 2: string+=","+povrayVector(normal)
        for i in xrange(len(self.parts.timeList1) - 1):
            # same code as above, changing curve2 and curve1
            xi,xip = self.parts.curve2.__call__(self.parts.timeList1[i]), self.parts.curve2.__call__(self.parts.timeList1[i + 1])
            yi=self.parts.curve1.__call__(self.parts.timeList2[i+1])
            normal=(-xi+yi).cross((self.parts.curve2.speed(self.parts.timeList2[i])))# if bad sign: artefact in the middle
            string+=","+povrayVector(normal)
            if i==len(self.parts.timeList1) - 2: string+=","+povrayVector(normal)
        string+="   }\n   face_indices {"+str(2*len(self.parts.timeList1)-2)
        for i in xrange(len(self.parts.timeList1)-1):
            string+=",<" +str(i)+ ","+ str(i+1)+","+str(i+len(self.parts.timeList1))+">"
            string+=",<"+str(i+1)+","+str(i+len(self.parts.timeList1))+","+str(i+1+len(self.parts.timeList1))+">\n"
        string+="}\n"+modifier(self,camera)+"}\n"
    elif isinstance(self,Prism) :
        #print(self)
        #string+="prism {\n  "+str(self.height(1))+","+str(self.height(2))+","+str(self.povrayNumberOfPoints)+",".join([point_to_povray2d(p,0,2) for p in self.polyline1]+[point_to_povray2d(p,0,2) for p in self.polyline2] )+" "+modifier(self,camera)+" }\n"
        string+="prism {\n  "+str(self.height1)+","+str(self.height2)+" , "+str(self.povrayNumberOfPoints)+","+",".join([point_to_povray2d(p,0,2) for p in self.polyline1] )+" "+" \n"
        string+=modifier(self,camera)+"}\n"
    elif isinstance(self,Polygon) :
        string+="polygon{"+str(len(self))+",+"
        for polygonPoint in self:
            string+=povrayVector(polygonPoint)
        string+=modifier(self,camera)+"}\n"
    return string   


def object_string_alone(self,camera):
    """
    This method builds the povray string for an object alone, without its chiddren.
    self is modified in the process but restauured at the end.
    Basically this part of code deals with csg operations. When there are no csg operations
    object_string_but_CSG is called. 
    """
    #print("before")
    if (not hasattr(self,"visibility")) or self.visibility<camera.visibilityLevel:
        #print(self.visibility)
        #print("invisible")
        #print(self)
        return ""
    #print("avant")
    todoList=copy.copy(self.csgOperations)# list to be restaured at the end
    #print("tdlist",len(todoList))
    try:
        todo=self.csgOperations.pop()
    except:
        return object_string_but_CSG(self,camera)
    slavesCopie=copy.copy(todo.csgSlaves)
    #for slave in slavesCopie:
    #    print(slave)
    #print("copie",len(slavesCopie))
    kw=todo.csgKeyword
    visibleSlaves=[slave for slave in slavesCopie if (slave.visibility>=camera.visibilityLevel and kw=="union") or (slave.booleanVisibility>=camera.visibilityLevel and ( kw=="difference" or kw=="intersection"))]
    for slave in visibleSlaves: #change restaured at the end
        slave.oldVisibility=slave.visibility
        slave.visibility=1
        #print(slave)
        #print(object_string_but_CSG(slave,camera))
    #print("keep visibility",len(visibleSlaves))
    #print("visibleSlaves",visibleSlaves)
    if todo.csgKeyword=="union":
        """ 
            Recall that in the union, the master is an empty objectInWorld.  Only the slaves participate in the physical object 
        If I'm not wrong the obect o is a compound iff o admits a union in its list of csg operations iff o has a unique union in its csg operations
        and this union is the first item. Indeed, when I add an intersection or difference, it is added at the end of the csg list of the master. And 
        for a union, we take a new empty objectInWorld with a unique csg op which is the union of the slaves. 
        """
        if len(visibleSlaves)>0:
            retour= "union {"+" ".join([object_string_alone(slave,camera)
                                        for slave in visibleSlaves])+" "+modifier_texture(self,camera) +" }"
            # remark that we add the modifier_texture of self, but not the modifier_matrix, otherwise the slaves would be moved at an incorrect positiion
        else:
            retour=""
    elif todo.csgKeyword=="difference" or todo.csgKeyword=="intersection":
        if len(visibleSlaves)>0:
            #print("visib0",visibleSlaves[0].visibility)
            retour= todo.csgKeyword+ " {"+object_string_alone(self,camera)+" ".join([object_string_alone(slave,camera) for slave in visibleSlaves]) +" }"
        else:
            retour=object_string_alone(self,camera)
    else:
        raise NameError('Unknown csg keyword')
    self.csgOperations=todoList
    for slave in visibleSlaves:
        slave.visibility=slave.oldVisibility
    return retour



def object_string_recursive(self,camera):
    """
    this function is the glue to call recursivly all children from the parent.
    The string for each element, parent or children, is done in  object_string_alone()
    """
    #print("self string rec",self.name)
    #print(self)
    #print(type(self))
    #print(isinstance(self,Cylinder))
    string=object_string_alone(self,camera)
    string+="\n\n"
 #   try:
        #print(self.__class__)
    #print(self.children)
    for child in self.children:
        string+=object_string_recursive(child,camera)
#    except:
#        raise ErrorName("stringRecursiveProblem")
    return string

def camera_string(camera):
    if camera.directFrame:
        orientationSign=-1
    else:
        orientationSign=1
    string= "camera { "+ camera.projection+"\nlocation "+povrayVector(camera.location)+\
            ' right '+ povrayVector(orientationSign*camera.imageWidth*X) + " up "+ povrayVector(camera.imageHeight*Y) +\
            " angle "+ str(camera.angle/math.pi*180)+ " sky "+povrayVector(camera.sky)+\
            " look_at "+ povrayVector(camera.lookAt) +" }\n\n"
    return string



def render(camera):
    booklet = open(camera.file, "w")
    booklet.write(camera.povrayPreamble)
    booklet.write(camera_string(camera))
    booklet.write(camera.povraylights+"\n\n")
    import gc
    if camera.filmAllActors:
        camera.actors+=[p for p in groupPhoto if p.parent==[] ]
    #for light in camera.lights:
    #    booklet.write("light_source {"+ povrayVector(light.location)+ " color White " + "}\n\n")
    for component in camera.actors:
        #prnit("chain for",component,povrayString(component))
        #print(component)
        booklet.write(object_string_recursive(component,camera))
    booklet.close()


