Bodies and Skeletons
---------------------------------
Bodies
==========================


.. image:: ./docPictures/skeleton.png


To check that the size of an object is compatible with a human body, we
can use the body primitive. The body has a crude appearance ( we shall
see later how to ameliorate it ) but it is
quite parametrizable to get precise dimensions. The following code
shows the possibie input parameters for the size and the instructions
to move the joints of the body.

When moving an articulation, you can choose to move it the standard way
or in the reverse way. For instance, using the shoulder, usually we move
the arm. But, in some exotic situation, it may happen the using the shoulder, 
the arm stays fixed and the rest of the body moves (for instance 
hanging rings in a gymnastice exercise). For each joint, there is
a side used by default, and an other side used if we set the option
"toggleJoint". 

The list of joints in the body is : "leftAnkle","rightAnkle","leftKnee",
            "rightKnee",
            "leftPelvis",
            "rightPelvis",
            "neck",
            "leftShoulder",
            "rightShoulder",
            "leftElbow",
            "rightElbow",
            "leftWrist",
            "rightWrist".


.. code-block:: python

    import armature
    from armature import *
    g=plane(Z,origin-Z).colored("Grey")
    body1=Body(topHeadHeight=1.805,
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
                 trunkUpperCirconference=1.03)   


    
    body2=Body().translate(X)
    body2.bend.leftShoulder(1.6,X) # arguments=(angleInRadians,axisVectorForTHeRotation) 
    body3=Body().translate(2*X)
    body3.bend.leftShoulder(1.6,X,toggleJoint=True)



Skeletons
==========================

For a nice looking picture, the above crude body is not sufficient.
There is a Skeleton class in Pycao to easily define
bodies different from the default body or more generally other skeletons.
    
	   
A skeleton in real life is a set of bones 
linked together by some joints.
To prescribe the position of a skeleton,
we have to take care that each bone has to stays 
linked to its joints. The "Skeleton" class 
helps to achieve this goal. 
 

To move a skeleton, we act with our muscles 
on the joint, and this is what we mimic in Pycao. 
To indicate that 
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

To declare a skeleton, we have to indicate

* the names of the bones , and for each name of a bone, an object to
  represent it in the 3D-picture 
* the names of the joints,
* for each joint name

  * the name of the 2 bones connected,
  * the default position for the center of the joint
  * the object used to represent it 
* The bone which is the ancestor of all the other bones.
    
Here is for instance a sequence of code used in the declaration of the
above body. We have prealably constructed objects
*leftFoot,rightFoot*,etc..., and then the body is constructed with the
following instructions.
    
.. code-block:: python

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

