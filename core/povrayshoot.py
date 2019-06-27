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
        string="\n//name: "+self.name+"\n"
    except AttributeError:
        string="\n//Unnamed Object\n"
    return string

# def compute_pigment(self):
#     #print(self,"in pigment")
#     if self.texture.color:
#         string= self.texture.color
#     elif self.texture.rgb:
#         i=self.texture.rgbIntensity
#         r=self.texture.rgb
#         string="rgb <"+str(i*r[0])+","+str(i*r[1])+","+str(i*r[2])+">"
#     else: return ""
#     return "pigment {"+string+"} "

# def compute_normal(self):
#     return ""#normal {brick   brick_size 1   mortar 0.02   scale 1}"# normal { bozo scale .01 bump_size 1} "
#     if hasattr(self,"normal"):
#         return self.normal
#     else: return ""

# def compute_finish(self):
#     if hasattr(self.texture,"diffuse"):
#         diffuse="diffuse "+str(self.texture.diffuse)+"\n" # this illuminates everything thus no shadow
#     else:
#         diffuse=""
#     if hasattr(self.texture,"ambient"):
#         ambient="ambient "+str(self.texture.ambient)+"\n" # for more light without shadow (thus no contrast)
#     else:
#         ambient=""
#     if hasattr(self.texture,"shadow"):
#         brilliance="brilliance "+str(self.texture.shadow)+"\n" # controls the intensity of the reflectedd light vs the angle of incidence
#     else:
#         brilliance=""
#         # thus increasing self.texture.dull increases the size of the shadowed region
#     #phong="phong "+str(self.texture.phong[0])+" phong_size "+str(self.texture.phong[1])+" " # finally I won't include this to keep simplicity
#     if hasattr(self.texture,"glintintensity"):
#         specular="specular "+str(self.texture.glintintensity)+" "
#         if hasattr(self.texture,"glintsize"):
#              specular+="roughness "+str(self.texture.glintsize)+"\n"
#     else:
#         specular=""
#     if hasattr(self.texture,"glintcolor"):
#         metallic="metallic {"+str(self.texture.glintcolor)+ "}\n"
#     else:
#         metallic=""
#     if hasattr(self.texture,"reflect"):
#         try:
#             reflection="reflection {"+str(self.texture.reflect[0],self.texture.reflect[1])+"}\n"
#         except:
#             reflection="reflection {"+str(self.texture.reflect)+"}\n"
#     else:
#         reflection=""
#     myFinish=diffuse+ambient+brilliance+specular+metallic+reflection
#     if myFinish:
#         string="finish {\n"+myFinish+"}"
#     else:
#         string=""
#     return string

# def texture_string(self):
#     string=""
#     if hasattr(self.texture,"povtexture"):
#         string=self.texture.povtexture+" "
#     string+=compute_pigment(self)
#     string+=compute_normal(self)
#     string+="matrix "+povrayMatrix(self.moveMap)
#     string+=compute_finish(self)

#     if string:
#         return "texture {"+string+"}"
#     else:
#         return ""


    
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


def texture_string(self,camera):
    "Returns a string describing the texture of the object"
    if self.visibility<camera.visibilityLevel:
        string=" no_shadow no_image no_reflection \n"
    else:
        return texture_string_cameraless(self)

def texture_string_cameraless(self):
    "Returns a string describing the texture of the object"
    string=""
    moveString=""
    if not hasattr(self,"texture"):
        return ""
    else:
        #myTexture=self.texture#
        # if hasattr(myTexture,"moveMap"):
        #     moveString=" matrix "+povrayMatrix(myTexture.moveMap)
        # if hasattr(myTexture,"name") and myTexture.name:
        #     string+=myTexture.name +moveString
        # else:
        #     string+=myTexture.declaration_string_bracketless()+moveString+"}"
        #string=" texture { "+string+" }\n"
        #print self
        #print hasattr(self,"texture")
        if hasattr(self,"texture") and self.texture is not None:
            return  self.texture.unnested_output(withMove=True)
        else: return  " "



def matrix_string(self):
    "Returns a string describing the matrix self.mapFromParts of the object"
    if isinstance(self,Primitive):
        string= ""
    else:
        string="matrix "+povrayMatrix(self.mapFromParts)
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
            openString=" open "
        else:
            openString=""
    if isinstance(self,Cylinder):
        string+="cylinder{"+povrayVector(self.parts.start)+","+povrayVector(self.parts.end)+","+str(self.parts.radius)+ openString+" "+modifier_string(self,camera)+"}"
    if isinstance(self,ICylinder):
        string+="quadric{"+povrayVector(vector(1,1,0))+","+povrayVector(vector(0,0,0))+"," +povrayVector(vector(0,0,0)) + ",-"+str(self.parts.radius**2)+ modifier_string(self,camera)+"}"
    elif isinstance(self,Torus) :
        string+="torus {\n"+str(self.parts.externalRadius)+","+str(self.parts.internalRadius)+" "+modifier_string(self,camera)+"}\n"
    elif isinstance(self,Cube) :
        string+="box {\n"+povrayVector(self.parts.start)+","+povrayVector(self.parts.end)+" "+modifier_string(self,camera)+"}\n"
    elif isinstance(self,RoundBox) :
        if self.merge:
            merge="0"
        else: merge="1"
        radius=str(self.radius)
        string+="object{Round_Box (\n"+povrayVector(self.parts.start)+","+povrayVector(self.parts.end)+","+radius+","+merge+")"+ " "+modifier_string(self,camera)+"}\n"
    elif isinstance(self,Sphere) :
        string+="sphere {\n"+povrayVector(self.parts.center)+","+str(self.parts.radius)+" "+modifier_string(self,camera)+"}\n"
    elif isinstance(self,AffinePlane) :
        string+="plane {\n"+povrayVector(self.normal)+","+str(-self[3]/self.normal.norm)+" "+modifier_string(self,camera)+"}\n"
        # Orientation Checked with the following code
        #s=Sphere(origin,.1).colored("Red")
        #p1=plane(Z,origin+.05*Z)
        #p1=plane(Z,origin-.05*Z)
        #p1=plane(-Z,origin+.05*Z)
        #p1=plane(-Z,origin-.05*Z)
        #s.intersected_by(p1)
    elif isinstance(self,Cone) :
        #print(self)
        string+="cone {\n"+povrayVector(self.parts.start)+","+str(self.parts.radius1)+"\n"+ povrayVector(self.parts.end)+","+str(self.parts.radius2)+" "+modifier_string(self,camera)+"}\n"
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
        #print(self)
        #string+="prism {\n  "+str(self.height(1))+","+str(self.height(2))+","+str(self.povrayNumberOfPoints)+",".join([point_to_povray2d(p,0,2) for p in self.polyline1]+[point_to_povray2d(p,0,2) for p in self.polyline2] )+" "+modifier_string(self,camera)+" }\n"
        string+="prism {\n  "+self.splineType+" "+str(self.height1)+","+str(self.height2)+" , "+str(self.povrayNumberOfPoints)+","+",".join([point_to_povray2d(p,0,2) for p in self.curve1] )+" "+" \n"
        string+=modifier_string(self,camera)+"}\n"
    elif isinstance(self,Polygon) :
        string+="polygon{"+str(len(self))+",+"
        for polygonPoint in self:
            string+=povrayVector(polygonPoint)
        string+=modifier_string(self,camera)+"}\n"
    return string   

def object_string_alone(self,camera):
    """
    This method builds the povray string for an object alone, without its chiddren.
    self is modified in the process but restauured at the end.
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
            retour+= "union {"+" ".join([object_string_alone(slave,camera)
                                        for slave in visibleSlaves])+" "+texture_string(self,camera) +" }"
            # remark that we add the texture_string of self, but not the matrix_string, otherwise the slaves would be moved at an incorrect positiion
        else:
            retour=""
    elif todo.csgKeyword=="difference" or todo.csgKeyword=="intersection":
        if len(visibleSlaves)>0:
            if hasattr(todo,"keepTexture") and todo.keepTexture==True:
                keepString=" cutaway_textures "
            else:
                keepString=""
                #print("visib0",visibleSlaves[0].visibility)
            retour= todo.csgKeyword+ " {"+object_string_alone(self,camera)+" ".join([object_string_alone(slave,camera) for slave in visibleSlaves]) +keepString+" }"
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
    string=object_string_alone(self,camera)
    string+="\n\n"
    for child in self.children:
        string+=object_string_recursive(child,camera)
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
    booklet.write(camera.preamble_string())
    booklet.write(globvars.userDefinedFunctions)
    booklet.write(camera_string(camera))
    material.build_textures_for_list(camera.actors)
    booklet.write(globvars.TextureString)
    booklet.write(camera.povraylights+"\n")
    for light in camera.lights:
        booklet.write(light.povray_string())
    import gc
    if camera.filmAllActors:
        camera.actors=[]
        for p in groupPhoto:
            #print("p et son parent")
            #print(p)
            #print(p.parent)
            if p.parent==[]:
                camera.actors.append(p)
        #print("la liste des acteurs",camera.actors)
        #camera.actors+=[p for p in  if p.parent==[] ]
    #for light in camera.lights:
    #    booklet.write("light_source {"+ povrayVector(light.location)+ " color White " + "}\n\n")
    for component in camera.actors:
        #print("chain for",component,object_string_recursive(component,camera))
        #print(component)
        booklet.write(object_string_recursive(component,camera))
    booklet.close()


