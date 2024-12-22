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
import material

def name_comment_string(self):
    try:
        #print("les suspects","\n//name: ",str(self.name),"\n")
        string="\n//name: "+self.name+"\n"
    except AttributeError:
        string="\n//Unnamed Object\n"
    return string

def scadVector(p):
    return("["+str(p[0])+","+str(p[1])+","+str(p[2])+"]")


def point_to_povray2d(p,i,j):
    " casts a vector v to the string '<v[i],v[j]>'"
    return("<"+str(p[i])+","+str(p[j])+">")


def scadMatrix(M):
    string="multmatrix(m = [ "
    for j in range(3):
        string+="["
        for i in range(4):
            string=string+str(M[j][i])
            if i<3: string=string+" , "
            if i==3: string+="],"
    string += "[0,0,0,1]])"
    return(string)


def texture_string(self,camera):
    "Returns a string describing the texture of the object"
    if self.visibility<camera.visibilityLevel:
        string=" no_shadow no_image no_reflection \n"
    else:
        return texture_string_cameraless(self)


    
def texture_string_cameraless(self):
    "Returns a string describing the texture of the object"
    string=""
    _moveString=""
    if not hasattr(self,"scad_color"):
        return ""
    else:
        return  self.scad_color




def matrix_string(self):
    "Returns a string describing the matrix self.mapFromParts of the object"
    if isinstance(self,AffinePlane):
        string=scadMatrix(self.mapFromParts*Map.rotational_difference(start=Z,end=self.normal,point1=origin,point2=self.markedPoint))
    elif isinstance(self,Cube):
        string=scadMatrix(self.mapFromParts*Map.translation(self.parts.start-origin))
    elif isinstance(self,RoundBox):
        string=scadMatrix(self.mapFromParts*Map.translation((self.parts.start+self.parts.end)/2-origin))
    elif isinstance(self,Sphere):
        string=scadMatrix(self.mapFromParts*Map.translation(self.center-origin))
    elif isinstance(self,Cylinder):
        string=scadMatrix(self.mapFromParts*Map.rotational_difference(start=Z,end=self.parts.rotaxis.p2-self.parts.rotaxis.p1,point1=origin,point2=self.parts.rotaxis.p1))
    elif isinstance(self,ICylinder):
        string=scadMatrix(self.mapFromParts)#*Map.translation((self.parts.axis.p1+self.parts.axis.p2)/2-origin-50*Z))
    elif isinstance(self,Cone):
        string=scadMatrix(self.mapFromParts*Map.rotational_difference(start=Z,end=self.parts.end-self.parts.start,point1=origin,point2=self.parts.start))
    elif isinstance(self,Torus):
        string=scadMatrix(self.mapFromParts*Map.rotational_difference(start=Z,end=Y))
    elif isinstance(self,Primitive):
        string= ""
    else:
        string=scadMatrix(self.mapFromParts)

    #return ""
    return string



def modifier_string(self,camera):
    "Returns a string describing the modifier of the object"
    return matrix_string(self)+texture_string(self,camera)




def object_string_but_CSG(self,camera):
    """
    This is the code to get the string for an object which has no csg operations. 
    """
    string=name_comment_string(self)
    if isinstance(self,Cylinder) or isinstance(self,Cone):
        if self.parts.open:
            print("WARNING: with open scad, cylinders and cones are always closed")
    if isinstance(self,Cylinder):
        string+=modifier_string(self,camera)+ "{ cylinder (h="+str((self.parts.rotaxis.p1-self.parts.rotaxis.p2).norm) +",r1="+str(self.parts.radius)+",r2="+str(self.parts.radius)+",center=false );}"
    if isinstance(self,ICylinder):
        string+=modifier_string(self,camera)+ "{ cylinder (h=100,r1="+str(self.parts.radius)+",r2="+str(self.parts.radius)+",center=true );}"
    elif isinstance(self,Torus) :
        string+=modifier_string(self,camera)+"{ rotate_extrude(convexity = 10) translate(["+str(self.parts.externalRadius)+", 0, 0]) circle(r ="+ str(self.parts.internalRadius)+",$fn=100 );}"
    elif isinstance(self,Cube) :
        string+=modifier_string(self,camera)+"{  cube ( size="+scadVector(self.parts.end-self.parts.start)+"); }\n"
    elif isinstance(self,RoundBox) :
        radius=str(self.radius)
        string+=modifier_string(self,camera)+"{ roundedBox(size="+scadVector(self.parts.end-self.parts.start)+",radius="+radius+ " );}\n"
    elif isinstance(self,Sphere) :
        string+=modifier_string(self,camera)+"{  sphere (r="+str(self.parts.radius)+");}\n"
    elif isinstance(self,AffinePlaneWithEquation) :
        string+=modifier_string(self,camera)+"{cube(size=[100,100,.001] ,center=true);}\n"
        print("WARNING: with open scad, planes do not exist they are  approximated with cubes 100unitsx100unitsx.001unit")
        # Orientation Checked with the following code
        #s=Sphere(origin,.1).colored("Red")
        #p1=plane(Z,origin+.05*Z)
        #p1=plane(Z,origin-.05*Z)
        #p1=plane(-Z,origin+.05*Z)
        #p1=plane(-Z,origin-.05*Z)
        #s.intersected_by(p1)
    elif isinstance(self,Cone) :
        string+=modifier_string(self,camera)+ "{ cylinder (h="+str((self.parts.end-self.parts.start).norm) +",r1="+str(self.parts.radius1)+",r2="+str(self.parts.radius2)+",center=false );}"
    elif isinstance(self,Lathe) :
        if isinstance(self.parts.curve,Polyline):
            latheType="linear_spline"
        elif isinstance(self.parts.curve,BezierCurve):
            latheType="bezier_spline"
        string+="lathe {\n"+latheType+" "+str(len(self.parts.curve))+"\n"
        for p in self.parts.curve: string+=","+point_to_povray2d(p,0,1)
        string+=modifier_string(self,camera)+"}\n"
    elif isinstance(self,RuledSurface):
        string+="mesh2 { vertex_vectors { "+str(2*len(self.parts.timeList1))+"\n"
        for t in self.parts.timeList1:
            string+=","+povrayVector(self.parts.curve1.__call__(t))
        string+="\n"
        for t in self.parts.timeList2:
            string+=","+povrayVector(self.parts.curve2.__call__(t))
            #print self.parts.curve1.__call__(t)
        string+=" }\n   normal_vectors { "+str(2*len(self.parts.timeList1))
        for i in range(len(self.parts.timeList1) - 1):
            xi,xip = self.parts.curve1.__call__(self.parts.timeList1[i]), self.parts.curve1.__call__(self.parts.timeList1[i + 1])
            yi=self.parts.curve2.__call__(self.parts.timeList2[i])
            #print("xi,yi,xip...",xi,yi,xip,xi-yi,xip-xi)
            #normal=(xi-yi).cross((xip-xi))
            normal=(xi-yi).cross((self.parts.curve1.speed(self.parts.timeList1[i])))
            #print(normal,"normal")
            #print(normal.normalized_clone())
            #print(normal.normalized_clone())
            string+=","+povrayVector(normal)
            if i==len(self.parts.timeList1) - 2: string+=","+povrayVector(normal)
        for i in range(len(self.parts.timeList1) - 1):
            # same code as above, changing curve2 and curve1
            xi,xip = self.parts.curve2.__call__(self.parts.timeList1[i]), self.parts.curve2.__call__(self.parts.timeList1[i + 1])
            yi=self.parts.curve1.__call__(self.parts.timeList2[i+1])
            normal=(-xi+yi).cross((self.parts.curve2.speed(self.parts.timeList2[i])))# if bad sign: artefact in the middle
            string+=","+povrayVector(normal)
            if i==len(self.parts.timeList1) - 2: string+=","+povrayVector(normal)
        string+="   }\n   face_indices {"+str(2*len(self.parts.timeList1)-2)
        for i in range(len(self.parts.timeList1)-1):
            string+=",<" +str(i)+ ","+ str(i+1)+","+str(i+len(self.parts.timeList1))+">"
            string+=",<"+str(i+1)+","+str(i+len(self.parts.timeList1))+","+str(i+1+len(self.parts.timeList1))+">\n"
        string+="}\n"+modifier_string(self,camera)+"}\n"
    elif isinstance(self,Prism) :
        #print(self.curve1)
        #string+="prism {\n  "+str(self.height(1))+","+str(self.height(2))+","+str(self.povrayNumberOfPoints)+",".join([point_to_povray2d(p,0,2) for p in self.polyline1]+[point_to_povray2d(p,0,2) for p in self.polyline2] )+" "+modifier_string(self,camera)+" }\n"
        string+="prism {\n  "+self.splineType+" "+str(self.height1)+","+str(self.height2)+" , "+str(self.povrayNumberOfPoints)+","+",".join([point_to_povray2d(p,0,2) for p in self.curve1] )+" "+" \n"
        string+=modifier_string(self,camera)+"}\n"
    elif isinstance(self,Polygon) :
        string+="polygon{"+str(len(self))+",+"
        for polygonPoint in self.controlPoints():
            string+=povrayVector(polygonPoint)
        string+=modifier_string(self,camera)+"}\n"
    return string   

def object_string_csg(self,camera):
    """
    This method builds the povray string (for an object alone, without its chiddren).
    self is modified in the process but restaured at the end.
    Basically this part of code deals with csg operations. When there are no csg operations
    object_string_but_CSG is called. 
    """
    if (not hasattr(self,"visibility")) or self.visibility<camera.visibilityLevel:
        return ""
    todoList=copy.copy(self.csgOperations)# list to be restaured at the end
    #print("tdlist",len(todoList))
    try:
        todo=self.csgOperations.pop()
    except:
        return object_string_but_CSG(self,camera)
    #slavesCopie=[copy.deepcopy(entry) for entry in todo.csgSlaves]
    slavesCopie=[entry.clone() for entry in todo.csgSlaves] #? should we clone without children here for efficiency ?? Probably
    #for slave in slavesCopie:
    #    print(slave) 
    #print("copie",len(slavesCopie))
    kw=todo.csgKeyword
    visibleSlaves=[slave for slave in slavesCopie if (hasattr(slave,"visibility") and slave.visibility>=camera.visibilityLevel and kw=="union") or (hasattr(slave,"booleanVisibility") and slave.booleanVisibility>=camera.visibilityLevel and ( kw=="difference" or kw=="intersection"))]
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
            retour="\n"+name_comment_string(self)
            retour+= "union() {"+" ".join([object_string_csg(slave,camera)
                                        for slave in visibleSlaves])+" "+texture_string(self,camera) +" }"
            # remark that we add the texture_string of self, but not the matrix_string, otherwise the slaves would be moved at an incorrect positiion
        else:
            retour=""
    elif todo.csgKeyword=="difference" or todo.csgKeyword=="intersection":
        if len(visibleSlaves)>0:
            #if hasattr(todo,"keepTexture") and todo.keepTexture==True:
            retour= todo.csgKeyword+ "() {"+object_string_csg(self,camera)+" ".join([object_string_csg(slave,camera) for slave in visibleSlaves]) +" }"
        else:
            retour=object_string_csg(self,camera)
    else:
        raise NameError('Unknown csg keyword')
    self.csgOperations=todoList
    for slave in visibleSlaves:
        slave.visibility=slave.oldVisibility
    return retour

def object_string_recursive(self,camera):
    """
    this function is the glue to call recursivly all children from the parent.
    The string for each element, parent or children, is done in  object_string_csg()
    """
    string=object_string_csg(self,camera)
    string+="\n\n"
    for child in self.children:
        string+=object_string_recursive(child,camera)
    return string

def camera_string(camera):
    if camera.directFrame:
        orientationSign=-1
    else:
        orientationSign=1
    #string= "camera { "+ camera.projection+"\nlocation "+povrayVector(camera.location)+\
      #      ' right '+ povrayVector(orientationSign*camera.imageWidth*X) + " up "+ povrayVector(camera.imageHeight*Y) +\
        #    " angle "+ str(camera.angle/math.pi*180)+ " sky "+povrayVector(camera.sky)+\
          #  " look_at "+ povrayVector(camera.lookAt) +" }\n\n"
    string="" # seems there is no camera in openscad
    return string


def render(camera):
    booklet = open(camera.file, "w")
    #booklet.write(camera.preamble_string())
    #booklet.write(globvars.userDefinedFunctions)
    #booklet.write(camera_string(camera))
    #material.build_textures_for_list(camera.actors)
    #booklet.write(globvars.TextureString)
    #booklet.write(camera.povraylights+"\n")
    #for light in camera.lights:
    #    booklet.write(light.povray_string())
    #import gc
    booklet.write(" use <MCAD/boxes.scad>;\n")       
    booklet.write("$fn=100;\n")
    if camera.filmAllActors:
        camera.actors=[]
        camera.idactors=[]
        for p in groupPhoto:
            #print("p et son parent")
            #print(p)
            #print(p.parent)
            #print(len(p.parent), "is length")
            # previously was type(p.parent)==[] but fails with p.parent=an numpy-array trying to cast and raising an error
            if type(p.parent)==list and len(p.parent)==0 and id(p) not in camera.idactors :
                camera.actors.append(p)
                camera.idactors.append(id(p))
        #print("la liste des acteurs",camera.actors)
        #camera.actors+=[p for p in  if p.parent==[] ]
    #for light in camera.lights:
    #    booklet.write("light_source {"+ povrayVector(light.location)+ " color White " + "}\n\n")
    for component in camera.actors:
        #print("chain for",component,object_string_recursive(component,camera))
        #print(component)
        booklet.write(object_string_recursive(component,camera))
    booklet.close()


