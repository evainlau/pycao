

"""
                MODULES IMPORT
"""


import os 
pycaoDir=os.environ["dirsubversion"]+"/articlesEtRechercheEnCours/pycao/distributed"
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
import povrayshoot 
from cameras import *
from lights import *

""" 
A skeleton in real life is a set of bones 
linked together by some joints. It is difficult 
to prescribe the position of a skeleton because 
we have to take care that each bone has to stays 
linked to its joints. The "Skeleton" class 
helps to achieve the description. 
 

To move a skeleton, we act with our muscles 
on the joint, and this is what we mimic in Pycao. 
For instance, using the shoulder 
it is possible to move our arm relativly to the rest of the body. 
In some exotic situation, it may happen the using the shoulder, 
the arm stays fixed and the rest of the body moves (for instance 
hanging rings in a gymnastice exercise). To indicate that 
we should by default move the arm rather than the rest of the body,  
we say that the bone in the arm is the child whether 
the bone in the trunk is the parent. 

In pycao, when a muscle acts on the joint of a Skeleton, 
the child bone moves (together with its descendants, as usual). 
Or to say it differently, all the bones and the joints which are 
on the child side of the joint  move simultaneaously. For instance, 
acting on a shoulder, the whole arm moves ( the humerus moves, and the radius and the
hand follow the movement, because they are children).

There is an ancestor in the genealogy, which is usually chosen to be 
the heavier bone of the body.  The genealogy is determined by the ancestor 
and the way the bones are connected. The order we meet the bones defines the 
genealogy.  For instance, if we choose the trunk to be the ancestor of the 
human body, then we first meet a leg, 
which is a child of the trunk, then a foot, which is a child of the leg.

If it happens that we want to move the parent side of the joint 
instead of the child side, as in the gym exercise, an option 
"toggleJoint" is offered. 



"""

class Skeleton(ObjectInWorld):

    def __init__(self,
                 joints=[["redJoint","bone0","bone1",None,None,Y],["pinkJoint","bone1","bone2",None,None,Y]],
                 bones=[["bone0",None],
                        ["bone1",None],
                        ["bone2",None]],
                 ancestor="bone1"):

        """
        Describe the parameters here: the graphical representations are not copied but passed by reference
        Each joint in joints is a list [joinName,boneName0,boneName1,point,object,vector]
        where names are strings, point is a point which is the center of the joint, object is the graphical representation, vector is the rotation axis by Default
        An entry of bones is ["nameOfThebone",graphicalObjectRepreseningBone]
        """
        #Since each joint is linked to two bones exactly (whereas a bone 
        #like the trunk of body may be attached to many articulations)  
        #we may represent a skeleton a graph whose segments parametrize 
        #joints and vertices parametrize bones. 
        ObjectInWorld.__init__(self)
        jointsInput=joints
        bonesInput=bones
        joints=Object()
        bones=Object()
        # Information for Joints only (not bones)
        for input in jointsInput:
            myJoint=input[4]
            myJoint.position=input[3].copy()
            myJoint.name=input[0]
            if len(input)>5: myJoint.rotationVector=input[5].copy()
            setattr(joints,myJoint.name,myJoint)
            #an alias to speeed-up input for the end-user
            setattr(self,input[0],myJoint)
        # Information for bones 
        for input in bonesInput:
            myBone=input[1]
            myBone.joints=[]
            myBone.name=input[0]
            setattr(bones,myBone.name,myBone)
        self.ancestor=getattr(bones,ancestor)
        self.ancestor.glued_on(self)
        #Constructing the tree from ancestor
        bonesDiscovered=[ancestor]
        while len(jointsInput)>0:
            for j in jointsInput:
                #print("j",j)
                #print("bonesDiscovered")
                #print(bonesDiscovered)
                #print(j[1] ,j[2])
                #print(j[1] in bonesDiscovered ,j[2] in bonesDiscovered )
                if j[2] in bonesDiscovered:
                    copie=j[2]
                    j[2]=j[1]
                    j[1]=copie
                if j[1] in bonesDiscovered:
                    jointObject=getattr(joints,j[0])
                    jointObject.parentBone=getattr(bones,j[1])
                    jointObject.childBone=getattr(bones,j[2])
                    jointObject.parentBone.joints.append(jointObject)
                    jointObject.childBone.joints.append(jointObject)
                    jointObject.childBone.glued_on(jointObject.parentBone)
                    #print(jointObject.childBone.name,"glued_on",jointObject.parentBone.name)
                    jointObject.position.glued_on(jointObject.parentBone)
                    jointObject.position.name="position"+jointObject.name
                    #print(jointObject.position.name,"glued_on",jointObject.parentBone.name)
                    jointObject.glued_on(jointObject.parentBone)
                    #print(jointObject.name,"glued_on",jointObject.parentBone.name)
                    #print("children de s",[c.name for c in self.ancestor.children])
                    if hasattr(jointObject,"rotationVector"):
                        jointObject.rotationVector.name="rotationVectorOf"+jointObject.name    
                        jointObject.rotationVector.glued_on(jointObject.parentBone)
                        jointObject.rotationVector.name="rotationVectorOf"+jointObject.name
                        #print(jointObject.rotationVector.name,"glued_on",jointObject.parentBone.name)
                    bonesDiscovered.append(j[2])
                    jointsInput.remove(j)
                #print("bonesDiscovered:")
                #print(bonesDiscovered)
        self.bones=bones
        self.joints=joints

    def _joint_move(self,joint,map,toggleJoint=False):
        """
        lowLevel function to move a joint
        """
        if toggleJoint:
            return Skeleton._joint_move_toggled(self,joint,map)
        joint.childBone.move(map)

            
    def _joint_move_toggled(self,joint,myMap):
        #print("toggled")
        #print(myMap)
        #print(s.pinkJoint.rotationVector,"spinkJoint.vector in Jmt")
        self.ancestor.move(myMap)
        Skeleton._joint_move(self,joint,myMap.inverse())
        
    def muscle_on_joint(self,joint,angle,rotationVector=None,keepParallel=[],toggleJoint=False):
        """
        keepParallel=a list of joints moved by the operations, no join being a descendant of an other
        """
        if hasattr(joint,"rotationVector") and rotationVector is None:
            rotationVector=joint.rotationVector
        #print(joint.position,rotationVector)
        rotationLine=Segment(joint.position,rotationVector)
        myMap=Map.rotation(rotationLine,angle)
        self._joint_move(joint,myMap,toggleJoint=toggleJoint)
        for myJoint in keepParallel:
            if toggleJoint:
               angle=-angle 
            if not myJoint.rotationVector == rotationVector:
                raise NameError("parallelel movement incompatible with the axis of the joint")
            self.muscle_on_joint(myJoint,-angle,rotationVector=rotationVector,toggleJoint=False)

    def move_alone(self,*args,**kwargs):
        return self
    # we pass because the armature is just a container.  The ancestor is glued on self, so it will move.

#s.muscle_on_joint(s.redJoint,math.pi/2,toggleJoint=True)
#print(s.pinkJoint.rotationVector,"spinkJoint.vector")
#print(s.pinkJoint.rotationVector,"spinkJoint.vector")

class Body(Skeleton):

    def __init__(self,
                 topHeadHeight=1.805,
                 armup=2.34, # the height of the end of the nails, when the arm is up
                 armdown=.69,# the height of the end of the nails, when the arm is down
                 topShoulder=1.54, #the height above the shoulder
                 bottomMentonHeight=1.57, 
                 headCirconference=.6,
                 neckCirconference=.4,
                 leftRightLegAxes=.12,# the distance between the legs axes, when they are parallels. 
                 leftRightArmAxes=.44, # idem for the arms
                 wristFinger=.22,# full distance from the wris to the end of  the nails, when the wrist is bent at 90 degrees 
                 elbowWrist=.325,# full distance from the wris to the elbow, when the wrist is bent at 90 degrees 
                 elbowFinger=.51,# lower arm, including elbow,
                 belowElbow=1.105,#, the height below the elbow, when the elbow is bent at 90 degrees horizontally
                 ankleHeight=.1,# the height of the proeminent point of the ankle
                 ankleWidth=.065,# measured at the proeminent points of the ankle
                 lowerLeg=.58, #ground to above the knee, when sit on a chair
                 upperLeg=.67, #distance from the back to to above the knee, when sit on a chair
                 leg=1.14,# sit on the ground, the back on a wall, distance from the wall to the foot arches
                 upperBody=.63, #height of the top of a shoulder, when sit on the ground
                 footSize=[.10,.28,None],
                 shoeSole=.02, # thickness of the sole
                 yDistanceAnkleToe=.2,# horizontal distance from the center of the ankle to the end of nails
                 handWidth=.1, 
                 handThickness=.025,
                 tibiaLowerCirconference=.24,
                 tibiaUpperCirconference=.37,
                 femurLowerCirconference=.4,
                 femurUpperCirconference=.62,
                 humerusLowerCirconference=.28,
                 humerusUpperCirconference=.36,
                 cubitusLowerCirconference=.175,
                 cubitusUpperCirconference=.30,
                 trunkLowerCirconference=.9,
                 trunkLowerWidth=.35,
                 trunkUpperCirconference=1.03):   


        #Computations 
        armLength=topShoulder-armdown#.83 is the value for the default parameters
        shoulderRadius=armLength-.5*(armup-armdown)#2.5
        headZSize=topHeadHeight-bottomMentonHeight#.235
        shoulderHeight=.5*(armup+armdown)#1.515
        wristRadius=.5*(elbowWrist+wristFinger-elbowFinger)#0.0175
        upperArm=topShoulder-belowElbow#.435
        lowerArm=elbowFinger#.51
        elbowRadius=.5*(upperArm+lowerArm-armLength)#.0474
        elbowHeight=belowElbow+.5*elbowRadius#=1.12875
        hand=wristFinger-2*wristRadius#0.185
        wristHeight=armdown+hand+wristRadius#.8925
        ankleRadius=.5*ankleWidth#.0325
        kneeRadius=.5*(upperLeg+lowerLeg-leg)#.055
        kneeHeight=lowerLeg-kneeRadius#.525
        pelvisRadius=.5*(leg+upperBody-topShoulder)#=.115
        pelvisHeight=leg-pelvisRadius#1.025

        #Geometric Objects
        neck=Cylinder(origin+(topShoulder-.0)*Z,origin+bottomMentonHeight*Z,neckCirconference/math.pi/2).colored("Red")
        head=Cylinder(origin,origin+(headZSize-headCirconference/math.pi/2)*Z,headCirconference/math.pi/2).move_against(neck,-Z,-Z,X,X).colored("Green")
        upperHead=Sphere(origin,headCirconference/math.pi/2).above(head).translate(-headCirconference/math.pi/2*Z).glued_on(head).colored("Green")
        for word in ["ankle","knee","pelvis"]:
            exec("left"+word.title()+"=Sphere(origin,"+str(eval(word+"Radius"))+").move_at(origin+"+str(eval(word+"Height"))+"*Z-"
                 +str(leftRightLegAxes*.5)+"*X).colored(\"Red\")")
            exec("right"+word.title()+"=left"+word.title()+".copy().translate("+str(leftRightLegAxes)+"*X)")
        for word in ["shoulder","elbow","wrist"]:
            exec("left"+word.title()+"=Sphere(origin,"+str(eval(word+"Radius"))+").move_at(origin+"+str(eval(word+"Height"))+"*Z-"
                 +str(leftRightArmAxes*.5)+"*X).colored(\"Red\")")
            exec("right"+word.title()+"=left"+word.title()+".copy().translate("+str(leftRightArmAxes)+"*X)")

            
        leftFoot=Cube(footSize[0],footSize[1],ankleHeight).colored("Blue")
        toCut=plane.from_3_points(leftFoot.point(0,.4,1),leftFoot.point(1,.4,1),leftFoot.point(.5,1,.2)).reverse()
        leftFoot.amputed_by(toCut)
        toCut=plane.from_3_points(leftFoot.point(0,.1,1),leftFoot.point(1,.1,1),leftFoot.point(.5,0,.2))
        leftFoot.amputed_by(toCut)
        leftFoot.to_Ankle=leftFoot.point(.5,yDistanceAnkleToe,1,"pnp")
        leftFoot.translate(leftAnkle.center-leftFoot.to_Ankle)
        leftSole=Cube(footSize[0],footSize[1],shoeSole).below(leftFoot).glued_on(leftFoot).colored("Orange")
        rightFoot=leftFoot.copy().translate(leftRightLegAxes*X)
        rightSole=leftSole.copy().translate(leftRightLegAxes*X).glued_on(rightFoot)

        slaves=[ Cylinder(origin+i*.20*handWidth*Y,origin+i*.25*handWidth*Y+.5*hand*Z,handThickness*.5) for i in range(4)]
        fingers=Compound(slaves)
        leftHand=Cube(handWidth,handThickness,.5*hand).colored("Blue")
        fingers.add_box(FrameBox([origin-0.5*handThickness*X,origin+handWidth*Y+0.5*handThickness*X+.5*hand*Z]),"initialBox")
        fingers.colored("Blue")
        fingers.move_against(leftHand,Z,Z,X,Y).glued_on(leftHand)
        fingers.rotate(Segment(leftHand.point(0,.5,0),leftHand.point(1,.5,0)),-math.pi/7)
        #lefthThumb=Cylinder(origin,origin+.3*hand*X,.5*handThickness).on_right_of(leftHand,adjustEdges=Z).colored("Blue").glued_on(leftHand)
        leftHand.below(leftWrist)

        
        rightHand=leftHand.copy()
        #rightThumb=Cylinder(origin,origin+.3*hand*X,.5*handThickness).on_left_of(rightHand,adjustEdges=Z).colored("Blue").glued_on(rightHand)
        rightHand.below(rightWrist)

        leftTibia=Cone(leftAnkle.center,leftKnee.center,tibiaLowerCirconference/math.pi/2,tibiaUpperCirconference/math.pi/2).colored("Yellow")
        leftFemur=Cone(leftKnee.center,leftPelvis.center,femurLowerCirconference/math.pi/2,femurUpperCirconference/math.pi/2).colored("Yellow")
        
        leftHumerus=Cone(leftElbow.center,leftShoulder.center,humerusLowerCirconference/math.pi/2,humerusUpperCirconference/math.pi/2).colored("Violet")
        leftCubitus=Cone(leftWrist.center,leftElbow.center,cubitusLowerCirconference/math.pi/2,cubitusUpperCirconference/math.pi/2).colored("Violet")

        trunk=Cone(origin,origin+(topShoulder-pelvisHeight)*Z,trunkLowerCirconference/math.pi/2,trunkUpperCirconference/math.pi/2).colored("Yellow")
        myRadius=0.51*(topShoulder-pelvisHeight)
        myCylinder=Cylinder(origin,origin+trunkLowerCirconference/math.pi*X,myRadius).above(trunk).translate(2*-myRadius*Z).colored("Yellow")
        trunk.intersected_by(myCylinder)
        resizeFactor=trunkLowerWidth*math.pi/trunkLowerCirconference
        trunk.scale(resizeFactor,1/resizeFactor,1)

        trunk.below(neck)

        for word in ["Tibia","Femur"]:
            exec("right"+word.title()+"=left"+word.title()+".copy().translate("+str(leftRightLegAxes)+"*X)")
        for word in ["Humerus","Cubitus"]:
            exec("right"+word.title()+"=left"+word.title()+".copy().translate("+str(leftRightArmAxes)+"*X)")
        bones=[["leftFoot",leftFoot],["rightFoot",rightFoot],["leftTibia",leftTibia],["rightTibia",rightTibia],["leftFemur",leftFemur],["rightFemur",rightFemur],["trunk",trunk],["head",head],["leftHumerus",leftHumerus],["rightHumerus",rightHumerus],["leftCubitus",leftCubitus],["rightCubitus",rightCubitus],["leftHand",leftHand],["rightHand",rightHand]]
        joints=[
            ["leftAnkle","leftFoot","leftTibia",leftAnkle.center,leftAnkle],
            ["rightAnkle","rightFoot","rightTibia",rightAnkle.center,rightAnkle],
            ["leftKnee","leftTibia","leftFemur",leftKnee.center,leftKnee],
            ["rightKnee","rightTibia","rightFemur",rightKnee.center,rightKnee],
            ["leftPelvis","leftFemur","trunk",leftPelvis.center,leftPelvis],
            ["rightPelvis","rightFemur","trunk",rightPelvis.center,rightPelvis],
            ["neck","head","trunk",neck.center,neck],
            ["leftShoulder","leftHumerus","trunk",leftShoulder.center,leftShoulder],
            ["rightShoulder","rightHumerus","trunk",rightShoulder.center,rightShoulder],
            ["leftElbow","leftCubitus","leftHumerus",leftElbow.center,leftElbow],
            ["rightElbow","rightCubitus","rightHumerus",rightElbow.center,rightElbow],
            ["leftWrist","leftHand","leftCubitus",leftWrist.center,leftWrist],
            ["rightWrist","rightHand","rightCubitus",rightWrist.center,rightWrist]]
        ancestor="trunk"
        Skeleton.__init__(self,joints,bones,ancestor)
        self.muscle_on_joint(self.rightWrist,-math.pi/4,Z)


#s.handle.translate(Z)
#s.redJoint.rotationVector=Z.copy()
#print(s.redJoint.rotationVector,"sredJoint.vector")
#s.muscle_on_joint(s.redJoint,math.pi/8,keepParallel=[s.pinkJoint],toggleJoint=False)

