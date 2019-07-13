

#pycaoDir="/home/laurent/subversion/evain/articlesEtRechercheEnCours/pycao/core"
#pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core"


"""
                MODULES IMPORT
"""


import os 
#pycaoDir=os.environ["dirsubversion"]+"/articlesEtRechercheEnCours/pycao/pycaogit/core"
import os
thisFileAbsName=os.path.abspath(__file__)
pycaoDir=os.path.dirname(thisFileAbsName)+"/../core"
import sys
from os.path import expanduser
sys.path.append(pycaoDir)
#print (pycaoDir)

import math



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


"""
                SCENE DESCRIPTION
"""

# a plane represented graphically as a half space 

if 1>0:  #bbloc1
   grayGround=plane(Z,origin).colored('Gray' ) # a plane with normal the vector Z=vector(0,0,1) containing the origin
   # The possible colors are the colors described in colors.inc in povray. 

   brownCube=Cube(1,2,2).colored("Brown") # The two opposite corners of the cube are origin and point(1,2,2)
   brownCube.translate(-2*X-Y) 
   
   closedPinkCylinder=Cylinder(start=origin+2*Y,end=origin+2*Y+.4*Z,radius=0.5).colored('SpicyPink')

   axis=line(point(0,-4,0),point(0,-4,1))
   infiniteYellowCylinder=ICylinder(axis,0.5).colored('Yellow') #an infinite cylinder of radius 0.5

   redSphere=Sphere(origin+.8*Z,.8).colored('Red') #arguments=center and radius

   silverWasher=Washer(point(3,3,0),point(3,3,0.3),.3,0.15).colored('Silver') #arguments; start,end,externalRadius,internalRadius
   
   blueOpenCylinder=Cylinder(start=origin+2*Y,end=origin+2*Y+0.3*Z,radius=0.5,booleanOpen=True) # a vertical Cylinder
   blueOpenCylinder.colored('Blue')
   blueOpenCylinder.translate(-4*X)

   yellowTorus=Torus(0.5,0.1,Z,origin)
   yellowTorus.named("Torus")
   p1=point(-2,0,0)
   p2=point(0,3,0)
   # The torus is sliced using two planes containing the axis and one point pi. 
   yellowTorus.sliced_by(p1,p2,acute=False).colored("Yellow").translate(-2*X+3.5*Y+0.5*Z)
   
   r=0.2
   curve=Polyline([origin,2*Y+X,Y+X,Y+2*X,-3*Y+X])# a polyline with control points prescribed. See the curve chapter for more details.
   cyanLathe=Lathe(curve).colored("Cyan").move(Map.affine(r*X,r*Z,r*Y,origin+2*X+1.4*Y))

   r=0.2
   curve=BezierCurve([origin,2*X+Y,X+Y,X+2*Y]) # A Bezier curve with control points prescribed. See the curve chapter for more details.
   orangeLathe=Lathe(curve).colored("Orange").move(Map.affine(r*X,r*Z,r*Y,origin+4*X))
   
   r=0.15
   curve=PiecewiseCurve.from_interpolation([origin+Y+2*X,3*Y+X,2*Y+X,Y+X,X],closeCurve=True)
   bronzeLathe=Lathe.fromPiecewiseCurve(curve).colored("Bronze").move(Map.affine(r*X,r*Z,r*Y,origin-4*X+.5*Z))
   
   p0=origin;
   p1=p0-X+Y;p2=p1+X+Y;p3=p2+X-Y;
   i=1.4
   # Below an interpolation curve through the control points
   curve4=PiecewiseCurve.from_interpolation([origin,p1,p2,p3,origin],closeCurve=True)
   curve7=PiecewiseCurve.from_interpolation([p2,p3,origin,p1,p2],closeCurve=True).scale(i,i,i).translate(1.7*Z)
   # The union of segments [curve7(t),curve4(t)]:
   HunterGreenRuledSurface=RuledSurface(curve7,curve4).colored("HuntersGreen").translate(-3.2*Y+3*X)

   violetCone=Cone(origin,origin+2*Z,.6,2 ).colored("Violet").translate(-4.5*X-4*Y)# arguments: start,end,radius1,radius2
   #ebloc1
   
   camera=Camera()
   directory=os.path.dirname(os.path.realpath(__file__))
   base=os.path.basename(__file__)
   camera.file=directory+"/docPictures/"+os.path.splitext(base)[0]+".pov"
   #camera.filmAllActors=True
   camera.location=origin+7*Y+3.2*Z
   camera.zoom(0.4)
   camera.lookAt=closedPinkCylinder.center
   l=Light().hooked_on(point(-2,0,6.8))
   l.intensity=2
   camera.actors=[grayGround,brownCube,closedPinkCylinder,infiniteYellowCylinder,violetCone,
                 redSphere,silverWasher,blueOpenCylinder,yellowTorus,cyanLathe,orangeLathe,bronzeLathe,HunterGreenRuledSurface]
   camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
   camera.pov_to_png # show the photo, ie calls povray. 



"""

    Retravail des box:
creer des fonctions box.insert(box,name) , box.select(name)
et gerer un dictionnaire self.dicobox.

Mettre un booleen seen dans Framebox et
remettre une adaptation de la fonction suivante
dans povrayshoot. 
def showBox(self):
   b=self.box()   
   liste=[b.plane(X,-.00001,"p"),b.plane(X,1.00001,"p"),b.plane(Y,-.00001,"p"),b.plane(Y,1.00001,"p"),b.plane(Z,-.00001,"p"),b.plane(Z,1.00001,"p")]
   # the above planes are slightly moved from their real location to avoid a dirty display when self has a face on one of the planes.
   colors=["SpringGreen","","","","",""]
   for i in range(6):
      liste[i].colored(colors[i])
   cube=liste. get(). intersect(liste)
   
         
def insert(self,framebox,name):
# cree la dicobox si ncr et la peuple si ncr
   if not hasattribute(self,dicobox):
      dicobox=Object()
      if hasattribute(self,box):
         dicobox.initialBox=self.box
   self.dicobox.name=framebox
   # the inserted box must move with the object
   framebox.glued_on(self)
   selectFramebox(self,name)
   
def selectFramebox,(self,name):
   if  self.dicobox.name.parent == self:
      # then the box is dyanmic and moves automatically with self
      self.box=lambda :self.dicobox.name
   else:
      # the box is a fixed marker
      self.box=lambda :  retrun self.dicobox.name.move(self.mapFromParts)

      
def listFramebox(self):
   print (self.dicobox.keys)

"""
