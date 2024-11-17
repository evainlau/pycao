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

# This is a very simple module that takes _parametrized_ curves from the picture,
# considers the projection of these curves on the plane $z=0$ 
# and generates the tixzfile corresponding to theses projections

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
    """
    Produces the name of self so that the file to be compiled is more  easily read and debugged
    """
    try:
        #print("les suspects","\n//name: ",str(self.name),"\n")
        string="\n//name: "+self.name+"\n"
    except AttributeError:
        string="\n%Unnamed Object\n"
    return string

def point_to_tikz2d(p,i,j):
    " casts a vector v to the string '(v[i],v[j])'"
    return("("+str(p[i])+","+str(p[j])+")")


def texture_string_cameraless(self):
    "Returns a string describing the texture of the object"
    string=""
    _moveString=""
    if not hasattr(self,"tikz_texture"):
        return "[ultra thick] "
    else:
        if hasattr(self,"tikz_texture") and self.tikz_texture is not None:
            return  self.tikz_texture
        else: return  " "

def texture_string(self,camera):
    "Returns a string describing the modifier of the object, basically thickness at the moment. Defined above but may be modified by a specific camera"
    if self.visibility<camera.visibilityLevel:
        return " "
    else:
        return texture_string_cameraless(self)


def object_string_but_CSG(self,camera):
    """
    This is the code to get the string for an object which has no csg operations. 
    """
    string=name_comment_string(self)
    if isinstance(self,ParametrizedCurve) :
        if isinstance(self,Polyline):
            myPolyline=self
        else:
            myPolyline=self.to_polyline()
        string+="    \draw "+texture_string(self,camera)
        string += "--".join([point_to_tikz2d(p,0,1) for p in myPolyline.controlPoints()])
        string += ";"
    return string   

def object_string_alone(self,camera):
    """
    This method builds the povray string for an object alone, without its chiddren nor csg
    self is modified in the process but restauured at the end.
    Basically this part of code deals with csg operations. When there are no csg operations
    object_string_but_CSG is called.  For curves dealed in this module, basically there are only unions
    not unions nor differences
    """
    if (not hasattr(self,"visibility")) or self.visibility<camera.visibilityLevel:
        return ""
    todoList=copy.copy(self.csgOperations)# list to be restaured at the end
    #print("tdlist",len(todoList))
    try:
        todo=self.csgOperations.pop()
    except:
        return object_string_but_CSG(self,camera) # si ya pas de csg, on renvoie seulement la chaine de l'objet simple
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
    if todo.csgKeyword=="union":
        """ 
            Recall that in the union, the master is an empty objectInWorld.  Only the slaves participate in the physical object 
        If I'm not wrong the obect o is a compound iff o admits a union in its list of csg operations iff o has a unique union in its csg operations
        and this union is the first item. Indeed, when I add an intersection or difference, it is added at the end of the csg list of the master. And 
        for a union, we take a new empty objectInWorld with a unique csg op which is the union of the slaves. 
        """
        if len(visibleSlaves)>0:
            retour="\n"+name_comment_string(self)
            retour+= "\n".join([object_string_alone(slave,camera)
                                        for slave in visibleSlaves])+" "+texture_string(self,camera) +" }"
            # remark that we add the texture_string of self, but not the matrix_string, otherwise the slaves would be moved at an incorrect positiion
        else:
            retour=""
    else:
        raise NameError('Unknown csg keyword, only unions for parametrized curves')
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


def render(camera):
    booklet = open(camera.file, "w")
    #print("ici dans render")
    booklet.write("\\documentclass{standalone}\\usepackage{tikz}\\begin{document}\\begin{tikzpicture}"
)
    booklet.write(globvars.userDefinedFunctions)
    if camera.filmAllActors:
        # build the list camera.actors with  all objects 
        camera.actors=[]
        camera.idactors=[]
        for p in groupPhoto:
            if p.parent==[] and id(p) not in camera.idactors:
                camera.actors.append(p)
                camera.idactors.append(id(p))
    for component in camera.actors:
        #print(component, "is component")
        booklet.write(object_string_recursive(component,camera))
    booklet.write( "\\end{tikzpicture}\\end{document}")
    booklet.close()


