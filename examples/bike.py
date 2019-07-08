

#pycaoDir="/home/laurent/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core/"
pycaoDir="/users/evain/subversion/articlesEtRechercheEnCours/pycao/pycaogit/core/"


"""
                MODULES IMPORT
"""


import os 
#pycaoDir=os.environ["dirsubversion"]+"/articlesEtRechercheEnCours/pycao/pycaogit/distributed/"
import sys
from os.path import expanduser
sys.path.append(pycaoDir)
#print (pycaoDir)
import math
import copy
from copy import copy


from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
from armature import *
import povrayshoot 
from cameras import *
from lights import *
from viewer import *

"""
                SCENE DESCRIPTION
"""

# a plane represented graphically as a half space 


light=Light() # a light
light.location=(origin+4.8*Z+2*X+5*Y)

if 1>0:
   import armature
   import bikelibrary
   from bikelibrary import *
   #######################################################################
                                  # PARAMETERS
   ###################################################################
   #meterial parameters
#######################
   metalThickness=.0015
   smallTubeRadius=.009
   mediumTubeRadius=.015
   largeTubeRadius=.025
   ##################
   # Body parameters
   #####################
   topHeadHeight=1.805
   armup=2.34 # the height of the end of the nails, when the arm is up
   armdown=.69# the height of the end of the nails, when the arm is down
   topShoulder=1.54 #the height above the shoulder
   bottomMentonHeight=1.57 
   headCirconference=.6
   neckCirconference=.4
   leftRightLegAxes=.12# the distance between the legs axes, when they are parallels. 
   leftRightArmAxes=.44 # idem for the arms
   wristFinger=.22# full distance from the wris to the end of  the nails, when the wrist is bent at 90 degrees 
   elbowWrist=.325# full distance from the wris to the elbow, when the wrist is bent at 90 degrees 
   elbowFinger=.51# lower arm including elbow,
   belowElbow=1.105#, the height below the elbow, when the elbow is bent at 90 degrees horizontally
   ankleHeight=.1# the height of the proeminent point of the ankle
   ankleWidth=.065# measured at the proeminent points of the ankle
   lowerLeg=.58 #ground to above the knee, when sit on a chair
   upperLeg=.67 #distance from the back to to above the knee, when sit on a chair
   leg=1.14# sit on the ground, the back on a wall, distance from the wall to the foot arches
   upperBody=.63 #height of the top of a shoulder, when sit on the ground
   footSize=[.10,.28,None]
   shoeSole=.02 # thickness of the sole
   yDistanceAnkleToe=.2# horizontal distance from the center of the ankle to the end of nails
   handWidth=.1 
   handThickness=.025
   tibiaLowerCirconference=.24
   tibiaUpperCirconference=.37
   femurLowerCirconference=.4
   femurUpperCirconference=.62
   humerusLowerCirconference=.28
   humerusUpperCirconference=.36
   cubitusLowerCirconference=.175
   cubitusUpperCirconference=.30
   trunkLowerCirconference=.9
   trunkLowerWidth=.35
   trunkUpperCirconference=1.03
   ##################
   # seat parameters
   ####################
   seatDimensions=[trunkLowerWidth+.05,.20,metalThickness]
   bodyAngle=math.pi*.2
   bodySupportHeight=.4
   bodySupportLength=bodySupportHeight/math.cos(bodyAngle)
   feetDistance=.20
   ################
   # Bike parameters
   ################
   trail1=-.3
   trail2=.35
   heightbs1=.18
   heightbs2=.32
   heightbs3=.18
   heightbs4=.32
   frontAngle=37*math.pi/180
   rearAngle=37*math.pi/180
   distanceSeatFrontWheel=.59
   distanceSeatRearWheel=.66
   distanceInterwheels=distanceSeatRearWheel+distanceSeatFrontWheel#1.20
   gardeAuSol=.15
   fEntrax=.1
   ################################################################
   #                 Starting the constuction !!
   ################################################################
   g=plane(Z,origin).colored("Brown")
   ########
   #Body
   ########
   body=Body().rotate(Segment(origin,origin+X),math.pi/4.6).translate(-.35*Z)
   legAngleAfter=atan(.5*feetDistance/body.leftPelvis.position[2])
   legAngleBefore=atan(.5*leftRightLegAxes/body.leftPelvis.position[2])
   angleForLegDistance=legAngleAfter-legAngleBefore
   body.bend.leftPelvis(+angleForLegDistance,Y)
   body.bend.rightPelvis(-angleForLegDistance,Y)
   body.bend.leftPelvis(math.pi/2+.12,X)
   body.bend.leftKnee(-math.pi/3-.15,X)
   body.bend.rightPelvis(math.pi/2*1.15,X)
   body.bend.rightKnee(-math.pi/4*1.3,X)
   body.bend.rightPelvis(-math.pi/20,X,toggleJoint=True)
   body.bend.leftShoulder(-math.pi/5,X)
   body.bend.leftElbow(math.pi/3,X)
   body.bend.rightShoulder(-math.pi/4.5,X)
   body.bend.rightElbow(math.pi/3,X)
   body.bend.neck(-math.pi/6,X)
   ################
   # seat and above
   ################
   seat=Cube(*seatDimensions).colored("Silver")
   bodySupport1=Cylinder(origin,origin+bodySupportHeight*Z,smallTubeRadius)
   bodySupport3=bodySupport1.clone()
   bodySupport1.above(seat,adjustEdges=-X,offset=.105*Y)
   bodySupport3.above(seat,adjustEdges=+X,offset=.105*Y)
   
   bodySupport1.rotate(Segment(bodySupport1.point(.5,.5,0),X),bodyAngle).translate((smallTubeRadius+metalThickness)*sin(bodyAngle)*Z)
   bodySupport1.colored("Bronze")
   bodySupport3.rotate(Segment(bodySupport1.point(.5,.5,0),X),bodyAngle).translate((smallTubeRadius+metalThickness)*sin(bodyAngle)*Z)
   bodySupport3.colored("Bronze")
   
   bodySupport2=bodySupport1.clone().translate(-.07*Y)
   bodySupport4=bodySupport3.clone().translate(-.07*Y)
   bodySupport1.glued_on(seat)
   bodySupport2.glued_on(seat)
   bodySupport3.glued_on(seat)
   bodySupport4.glued_on(seat)

   bodyContactSeat=.5*(body.leftPelvis.center+body.rightPelvis.center)
   seat.translate(bodyContactSeat-seat.point(.5,.5,1)-body.pelvisRadius*Z)
   #print(bodyContactSeat[1]-wheel1.center[1])

   #########################
   # wheels
   ##########################
   wheel1=RearWheel().rotate(Segment(origin,origin+Z),math.pi/2)
   wheel2=FrontWheel().rotate(Segment(origin,origin+Z),math.pi/2)
   wheel1.translate(origin-wheel1.tyre.point(.5,.5,0)+(distanceSeatFrontWheel-.65)*Y)
   wheel2.translate(origin-wheel2.tyre.point(.5,.5,0)-distanceInterwheels*Y)
   #wheel1.tyre.show_box().glued_on(wheel1)
   contactWheel1=wheel1.tyre.point(.5,.5,0)
   contactWheel2=wheel2.tyre.point(.5,.5,0)

   ###############################
   #  Steering Axis  and below seat
   #############################
   # fsa=frontSteeringAxis, rsa=RearsteeringAxis
   fsa=Segment(contactWheel1,contactWheel1+1*(Z-math.tan(frontAngle)*Y)).translate(trail1*Y)
   rsa=Segment(contactWheel2,contactWheel2+1*(Z+math.tan(frontAngle)*Y)).translate(trail2*Y)
   fsatop=Point.from_plane_and_line(plane(Z,seat.point(.5,.5,0)),fsa)
   rsatop=Point.from_plane_and_line(plane(Z,seat.point(.5,.5,0)),rsa)
   fsadown=Point.from_plane_and_line(plane(Z,origin+(gardeAuSol+.03)*Z),fsa)
   rsadown=Point.from_plane_and_line(plane(Z,origin+(gardeAuSol+.03)*Z),rsa)
   frontLength=(fsatop-fsadown).norm
   rearLength=(rsatop-rsadown).norm
   fcyl=Cylinder(origin,origin+frontLength*Z,largeTubeRadius).colored("Violet")
   rcyl=Cylinder(origin,origin+rearLength*Z,largeTubeRadius).colored("Violet")
   fPoint=fcyl.point(.5,0,1).translate(-.05*Z)
   rPoint=rcyl.point(.5,1,1).translate(-.05*Z)
   fPointLower=fPoint.clone().translate(-.05*Z)
   rPointLower=rPoint.clone().translate(-.05*Z)
   fp2cut1=plane(Z,fPoint)
   rp2cut1=plane(Z,rPoint)
   #fp2cut1.rotate(Segment(fPoint,X),-frontAngle)
   fp2cut2=plane(-Z,fPointLower)
   rp2cut2=plane(-Z,rPointLower)
   fp2cut2.rotate(Segment(fPointLower,X),-frontAngle)
   rp2cut2.rotate(Segment(rPointLower,X),rearAngle)
   fp2cut3=plane(-Y,fcyl.point(.5,.5,.5))
   rp2cut3=plane(Y,rcyl.point(.5,.5,.5))
   ftoCut=fp2cut3.intersected_by([fp2cut1,fp2cut2])
   rtoCut=rp2cut3.intersected_by([rp2cut1,rp2cut2])
   fcyl.amputed_by([ftoCut])
   rcyl.amputed_by([rtoCut])
   
   
   fcyl.screw_on(fsa,adjustAlong=[fcyl.point(.5,0,1),fsatop]).glued_on(seat)
   rcyl.screw_on(rsa,adjustAlong=[rcyl.point(.5,0,1),rsatop]).glued_on(seat)
   bcyl=Cylinder(fcyl.point(.5,.5,.02,"ppa"),rcyl.point(.5,.5,.02,"ppa"),mediumTubeRadius).glued_on(seat).colored("Violet")

   interPelvis=(body.leftPelvis.position-body.rightPelvis.position).norm
   rightSupport=Cylinder(bcyl.point(.5,.25,.5),seat.point(.5,.5,0)+interPelvis*X,smallTubeRadius).colored("Red").glued_on(seat)
   leftSupport=Cylinder(bcyl.point(.5,.75,.5),seat.point(.5,.5,0)-interPelvis*X,smallTubeRadius).colored("Red").glued_on(seat)

   ################
   #  front part
   ################
   ped=Crankset().against(wheel1,-Y,-Z,X,X)
   ped.translate(+.30*Y-.03*Z)
   ped.rotate(ped.axis(),math.pi/1.8)
   externalRadius=(ped.center-wheel1.tyre.center).norm-.04
   internalRadius=mediumTubeRadius
   endAxis=fcyl.point(.5,.5,-.05,"ppa")
   # torus from crankset towards body
   Torus(externalRadius,internalRadius,X,wheel1.tyre.center).sliced_by(ped.center+.1*Y,fcyl.point(.5,.5,0)-.05*Z).glued_on(ped).colored("Aquamarine")
   # torus from crankset to front bike
   #Torus(externalRadius,internalRadius,X,wheel1.tyre.center).sliced_by(ped.center,ped.center-.5*Z).glued_on(ped).colored("Aquamarine")
   # the cylinder in fcyl
   inFcyl=Cylinder(fcyl.point(.5,.5,1),endAxis,mediumTubeRadius).glued_on(ped).colored("Aquamarine")
   toCut=fcyl.boxplane(-Z,.05,"a").intersected_by(fcyl.boxplane(Z,.09,"a"))
   inFcyl.amputed_by(toCut)
   #The upper joint to the torus
   Cylinder(fcyl.point(.5,.5,.7),fcyl.point(.5,.5,.7)+.1*Y,mediumTubeRadius).glued_on(ped).colored("Aquamarine")
   # The lower joint to the torus
   Cylinder(endAxis-.01*(Y+Z),endAxis+.05*(Y+Z),mediumTubeRadius).glued_on(ped).colored("Aquamarine")

   #fork1=Fork(legLength=.35,upperTubeRadius=smallTubeRadius,lowerTubeRadius=smallTubeRadius,headLength=0,headRadius=.02,entrax=.1)
   fork2=Fork(legLength=.43,upperTubeRadius=smallTubeRadius,lowerTubeRadius=smallTubeRadius,headLength=0,headRadius=.02,entrax=.1)
   fork3=Fork(legLength=.39,upperTubeRadius=smallTubeRadius,lowerTubeRadius=smallTubeRadius,headLength=0,headRadius=.02,entrax=.1)
   fork4=Fork(legLength=.39,upperTubeRadius=smallTubeRadius,lowerTubeRadius=smallTubeRadius,headLength=0,headRadius=.02,entrax=.1)
   #fork3=fork1.copy()
   #for element in ["fork2","fork3"]:
    #  exec(element+".colored(\"Aquamarine\").glued_on(seat)")
   #fork1.screw_on(Segment(wheel1.center,Z),adjustAlong=[fork1.junction,wheel1.center+externalRadius*Z]).colored("Aquamarine").glued_on(seat)
   vector=(fcyl.point(.5,.5,-.05,"ppa")-wheel1.center).normalized_clone()
   fork2.screw_on(Segment(wheel1.center+.02*Z,vector),adjustAlong=[fork2.junction,fcyl.point(.5,.5,0,"ppa")]).colored("Aquamarine").glued_on(seat)
   vector=.75*Y+.55*Z
   fork3.screw_on(Segment(wheel1.center+.02*Z,vector),adjustAlong=[fork3.junction,wheel1.center+externalRadius*vector.normalized_clone()]).colored("Aquamarine").glued_on(seat)
   vector=-1.4*Y+2*Z
   fork4.screw_on(Segment(wheel1.center+.02*Z,vector),adjustAlong=[fork4.junction,wheel1.center+externalRadius*vector.normalized_clone()]).colored("Aquamarine").glued_on(seat)
   dropoutOffset=.015*Z
   dropout1=Cube(.09,metalThickness,.07).colored("Aquamarine")
   dropout2=dropout1.clone()
   dropout1.behind(wheel1,offset=dropoutOffset).glued_on(seat)
   dropout2.in_front_of(wheel1,offset=dropoutOffset).glued_on(seat)

   ################
   # rear part
   ################
   endAxis=rcyl.point(.5,.5,-.05,"ppa")
   inRcyl=Cylinder(rcyl.point(.5,.5,1),endAxis,mediumTubeRadius).glued_on(ped).colored("Aquamarine")
   toCut=rcyl.boxplane(-Z,.05,"a").intersected_by(rcyl.boxplane(Z,.09,"a"))
   inRcyl.amputed_by(toCut).glued_on(seat)
   rfork2=Fork(legLength=.50,upperTubeRadius=smallTubeRadius,lowerTubeRadius=smallTubeRadius,headLength=0,headRadius=.02,entrax=.135)
   vector=(rcyl.point(.5,.5,-.03,"ppa")-wheel2.center).normalized_clone()
   rfork2.screw_on(Segment(wheel2.center+.03*Z,vector),adjustAlong=[rfork2.junction,rcyl.point(.5,.5,-.03,"ppa")]).colored("Aquamarine").glued_on(seat)
   rfork3=Fork(legLength=.55,upperTubeRadius=smallTubeRadius,lowerTubeRadius=smallTubeRadius,headLength=0,headRadius=.02,entrax=.135)
   vector=(rcyl.point(.5,.5,.05,"ppn")-wheel2.center-.05*Z).normalized_clone()
   rfork3.screw_on(Segment(wheel2.center+.05*Z,vector),adjustAlong=[rfork3.junction,rcyl.point(.5,.0,.01,"ppn")]).colored("Aquamarine").glued_on(seat)

   dropout3=Cube(.09,metalThickness,.09).colored("Aquamarine")
   dropout4=dropout3.clone()
   dropout3.behind(wheel2,offset=dropoutOffset).glued_on(seat)
   dropout4.in_front_of(wheel2,offset=dropoutOffset).glued_on(seat)

   cyl1=Cylinder(contactWheel1,contactWheel1+.4*(Z-math.tan(frontAngle)*Y),.01)
   cyl2=Cylinder(contactWheel2,contactWheel2+.4*(Z+math.tan(rearAngle)*Y),.01)

   
   bearing=Bearing()
   bearing2=Bearing()   
   bs1=BearingSupport(bearing,cyl1)
   bs1.place_on_axis(cyl1.axis(),heightbs1,front=Y)
   bearing.place_on_support(bs1).glued_on(bs1)
   bs2=BearingSupport(bearing2,cyl2)
   #bs2=bs1.clone()
   bs3=BearingSupport(bearing2,cyl2)
   bs4=BearingSupport(bearing2,cyl2)

   a=Compound([["name",origin],origin+Z])
   #bs2=a.clone()
   bs2=bs2.place_on_axis(cyl1.axis(),heightbs2,front=Y)
   bs3=bs3.place_on_axis(cyl2.axis(),heightbs3,front=-Y)
   bs4=bs4.place_on_axis(cyl2.axis(),heightbs4,front=-Y)
   
   #body.bones.rightHand.visibility=0
   #print ((bs2.support.center-bs4.support.center).norm)
   camera=Camera()
   camera.file="bike.pov"
   camera.filmAllActors=False
   #camera.projection="orthographic"
   #camera.filmAllActors=True
   #camera.location=origin+.8*Z-1*X; camera.zoom(.161812525)
   #camera.location=origin-.5*Y-.2*X+0.4*Z

  
   #camera.lookAt=self.bracketAxis.center
   camera.lookAt=.5*(wheel1.tyre.center+wheel2.tyre.center)
   camera.lookAt=body.leftPelvis.center
   camera.povraylights=camera.povraylights+"  light_source {<1000,1000,-1000>, rgb <1,0.75,0>   }"
   #perspectiveView
   #camera.location=point(-2.17,1.14,1.62);camera.lookAt=point(0.1,-0.51,0.45);camera.angle=0.5
   #front View
   camera.location=point(-2.9,-0.51,0.45);camera.lookAt=point(0.08,-0.01,0.45);camera.angle=0.4
   #camera.location=origin+.31*Y+0*X+2.8*Z;
   camera.zoom(.2861812525)
   camera.actors=[body,seat,wheel1,wheel2,cyl1,cyl2,bs1,bs2,bs3,bs4,g,ped]
   #camera.actors=[seat,wheel1,wheel2,g,ped]
   #camera.actors=[inRcyl]
   camera.povraylights=camera.povraylights+"  light_source {<"+str(camera.location[0])+","+str(camera.location[1])+","+str(camera.location[2])+">, rgb <.3,0.35,0.3>   }"
   camera.imageHeight=800 # in pixels
   camera.imageWidth=1000
   camera.quality=11
   camera.shoot
   #print(seat.center)
   camera.silent=False
   camera.show
   #ViewerWindow(camera)


