Bodies and Skeletons
---------------------------------
Bodies
==========================


.. image:: ./generatedImages/skeletons.png


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

.. literalinclude:: skeletons.py
   :start-after: bbloc1
   :end-before: ebloc1


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


.. literalinclude:: armature.py
   :start-after: bbloc1
   :end-before: ebloc1
