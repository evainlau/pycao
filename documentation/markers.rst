****************************************************************
Markers
****************************************************************

Types of Markers
======================

The markers are the analogs of the marks drawn by a carpenter
on its piece of wood. They are are used as reference for further
construction. There are several types of markers :

- hooks : the markers are points
- lines
- boxes ( useful to specify parallepedical coordinates)  
- cylboxes ( useful to specify cylindrical coordinates)
  
An object may carry many markers, many hooks, lines or boxes,
but exactly one of each type is selected and active. When you add
a marker, it is automatically selected. For instance

.. code-block:: python
		
   c.add_axis("myFirstAxis",line(origin,origin+X))
   c.add_axis("mySecondAxis",line(origin,origin+X+Y))

will add 2 axis markers to the object, the last added axis being
the selected one. We can refer to the markers as follow:

.. code-block:: python
		
   c.axis() # the selected axis
   c.axis.myFirstAxis 
   c.axis("myFirstAxis") # same output as the previous line

To change the selected axis

.. code-block:: python
		
   c.select_axis("myFirstAxis")

Similarly, for hooks and boxes, the following instructions make sense:

.. code-block:: python
		
   c.box() # the selected box
   c.box.myBoxName
   c.box("myBoxName")
   c.select_box("myBoxName")
   c.hook()
   c.hook.hookName
   c.hook("hookName")
   c.select_hook("hookName")


Hooks and Lines 
====================
  
We have already encountered hooks and lines markers and we saw
that they are used to move an object geometrically in the functions
hooked_on, self_grotate, etc ... 


Boxes
========


A common way to specify the positions of the objects in a
workshop is to draw marks on the objects from which we make
measurements. For instance, we draw a circle, and we drill
our object 2 centimeters above the circle.

In pycao, we can attach boxes to our objects.
The purpose of boxes is to allow various ways to make measurements.
The boxes are not shown on the 3D-view. They are just marks useful
for our constructions. 

We can attach any number of boxes to an object. The boxes may
have different form,  parallelipedic or cylindric for instance.
The first one is useful for measurements in parallelipedic
coordinates, the second one for measurements in cylindrical
coordinates.

In the real life there are several ways to make a measurement
with the same marks on our piece of wood.
For instance, if we have drawn a square,
sometimes we measure 2 centimeters from the left side of the square, or from the
right side of the square. Sometimes, we use no reference to meters or
centimeters, yet we use our marks, for instance when we 
we consider the point in the middle of the square. 
In pycao, we may specify a letter "a", "n" or "p" for some parameters
to indicate how we want to make measurements with our boxes. 

To sum up, in Pycao, there is a concept of box. A box is like some sketch/contour of a 3D-object
drawn on your piece that we can use to make several type of
measurements. 

Usual ( parallelipedic ) boxes
================================

Points in Boxes
-------------------

In general, a box has three coordinates and the
instruction

.. code-block:: python
		
   c.point(x,y,z)

denotes the points of coordinates (x,y,z) with respect to the selected
box of the object. Options are possible, and here are somme possibilities.

.. code-block:: python
		
   c.point(x,y,z."aaa")
   c.point(x,y,z."nap")
   c.point(x,y,z."ppp")
   c.point(x,y,z."pna")
   c.point(x,y,z) # an alias for c.point(x,y,z,"ppp")

Let us explain the previous notation.
When we make a measurement of a piece of wood on the desk, sometimes we start from
the left side ("5 centimeters from the left side of the desk") sometimes from the
right side ("5 centimeters from the right side") sometimes we
describe the points in terms of proportionality ("in the middle
between the left side and the right side"). These three possibility of
measurements are possible inside a box with pycao. They correspond to
the letters "a" (for
absolute), "n" (for negative) and "p" (for proportional) in the
strings above. And you can mix the units of measurements on each axis. For instance,
if you choose "anp", ie absolute for x, negative for y and proportional for
z, a point with coordinate  p=c.point(.5,.5,.5,"anp")
will be inside the box .5 units from the face with minimal x,
.5 units from the face with maximal y, and in the middle of the
the two planes with constant z. 


.. image:: ./docPictures/markers1.png

To illustrate these notations, we draw a little
drawer. 


.. literalinclude:: markers1.py
   :start-after: bbloc1
   :end-before: ebloc1

    

Lines and planes in a box
-----------------------------------

We have seen the notations to describe a point relative to a box. 
Similarly, planes parallel to the facets and lines perpendicular to
the facets of the box of a bounded objects are easily accessible
to be used as intermediate steps of the construction.

Here is an example, 
where we draw infinite cylinders along the lines and an orange plane
in coordinates relative to the box of the cube. 

.. image:: ./docPictures/markers2.png

The instructions are:

.. code-block:: python

   c.boxline.(x,y,z,"rs") # r,s have value a,n or p according to the frame used.
   c.boxplane((A,"r") #  with A=+/- X,Y or Z, r="a","n" or "p"
   
The coordinate  that moves along the line is described as "None".The example for the image above
clarifies. 


.. literalinclude:: markers2.py
   :start-after: bbloc1
   :end-before: ebloc1


Adding new boxes
------------------------------------

The code to define a box is

.. code-block:: python

   Framebox(listOfPpoints)
   
Here is an example of code to add boxes, and select one.


.. code-block:: python
   
   firstBox=FrameBox([origin,point(2,5,7), point(1,1,1)]) # The smallest box containing the points in the list
   secondBox=FrameBox([origin, point(-1,1,1)]) #  An other box
   myObject=point(0,0,0)
   myObject.add_box("newbox",firstBox) # adds the box to the point and select it 
   print(myObject.box())
   myObject.add_box("mySecondBox",secondBox)
   print (myObject.box()) # returns the information on the second Box
   myObject.print_boxes() #  the names of the boxes of a
   myObject.select_box("newbox") # selects firstBox again
   print (myObject.box())

The output is:

.. code-block:: python

		FrameBox:
		Origin: Affine Point  [0.0,0.0,0.0]
		Vectors:
		Vector  [2.0,0.0,0.0] 
		Vector  [0.0,5.0,0.0] 
		Vector  [0.0,0.0,7.0] 

		FrameBox:
		Origin: Affine Point  [-1.0,0.0,0.0]
		Vectors:
		Vector  [1.0,0.0,0.0] 
		Vector  [0.0,1.0,0.0] 
		Vector  [0.0,0.0,1.0] 

		['mySecondBox', 'newbox']
		FrameBox:
		Origin: Affine Point  [0.0,0.0,0.0]
		Vectors:
		Vector  [2.0,0.0,0.0] 
		Vector  [0.0,5.0,0.0] 
		Vector  [0.0,0.0,7.0] 



		



Visualize the current box
---------------------------------

We may visualize a box when
we do not remember its size or its orientation. 
As an example, we draw
two  spheres s,t, and we show the box of the small sphere s.

Note that the colors of
the facets correspond to the local
axis of the object (XYZ corresponds to the  colors RGB).
A half cylinder indicates the positive direction on each coordinate.
For instance, for the small sphere in the box, the local Y coordinates
is in front of us, along the green cylinder. 
(Not seen on this picture: The 
side facing the negative coordinates is lighter than the facet
which faces the positive coordinates) 


.. image:: ./docPictures/markers3.png


.. literalinclude:: markers3.py
   :start-after: bbloc1
   :end-before: ebloc1


Stacking boxes
-----------------------

Sometimes, we want to stack objects, which mean the we stack their
implicit box. For instance, to put a cube above a cylinder, proceed as follows

.. image:: ./docPictures/markers4.png


.. literalinclude:: markers4.py
   :start-after: bbloc1
   :end-before: ebloc1

    
Similarly, there are commands

.. code-block:: python
		
   object1.below(object2)
   object1.on_left_of(object2)
   object1.on_right_of(object2)
   object1.in_front_of(object2)
   object1.behind(object2)


These notations are useful only if you use the geometric conventions
of Pycao : Z is vertical, Y is in front of you, and X on the right. 
So that the instructions are geomoetric if you look an object at
position P from the position P-c*Y, with c>0. 



Cylboxes (aka cylindrical boxes)
=======================================

A cylbox is the contour of a cylinder of finite length. The cylinder
has a marked point which is used as the origin of the measurement of
the angles in cylindrical coordinates, ie the marked point has by
definition an angle or a winding number equal to zero.

The formalism is quite similar to the formalism of parallelipedic
boxes. We can add,select,... cylboxes. If the cylbox is vertical
with a horizontal plane just below,
a point with coordinate (r,w,s) with respect to that cylbox
is at distance r from the axis, s from the horizontal
plane, and the winding number is w. The numbers r,s can be interpreted
with the letters "a,p,n" as for regular boxes. The winding number on
the other hand, is always absolute. 

If an object c carries a cylbox, the instruction

.. code-block:: python

    c.cylpoint(r,w,s)
    c.cylpoint(r,w,s,"xy") # x,y in "anp"

will make sense and denote a point. A cylinder carries a cylbox by
default (which is itself) at the time of construction. 

.. image:: docPictures/markers5.png



Let's use these coordinates to build the above watch. 


.. literalinclude:: markers5.py
   :start-after: bbloc1
   :end-before: ebloc1


.. 
    The drawings of young children are usually made with spheres (for the 
    head of a person,top of a tree), cylinders (trunk of a tree,legs)
    and cubes (house). 

    Similarly, to put 
    a broom along the wall means imlicitly that the broom is assimilated 
    to a cylindre because of the broom handle, and it is asked 
    to put the axis of the cylindre parallel to the wall. 

    Thus, spheres, cylinders and cubes are deeply in our mind.
    We often assimilate the objects with pure forms 
    like children when we orientate objects. 
    This is what we reproduce in pycao. 

    This will make sense provided the objects are bounded. We simply move 
    the bounding box of myObject against the bounding box of
    anOtherObject. Similarly,  an object of revolution 
    or an object with a particular axis is orientable via its axis. 

..
   When someones asks to put a sofa parallel to a
   wall, the sofa is assimilated to a cube and what is asked is 
   to put one edge parallel to the walll.  In Pycao,
   we mimic the natural language :
   We assimilate an object to its box, or equivalently
   we move the box and we carry the object in the box. 

   As an example, we consider the following scene. 

   .. image:: ./docPictures/table.png

   .. code-block:: table

      # The dimensions/constants used are in the next 6 lines
      ################
      tableTrayDimensions=Vector(1,.5,.05)
      tableLegDimensions=Vector(.2,.03,.8)
      placementVector=X+Y
      flowerPotRadius=0.1
      flowerPotHeight=0.3
      flowerPotThickness=0.01

      # Describing the scene starts here
      ################
      ground=plane(-Z,origin).colored("Grey") # a plane with normal vector Z=(0,0,1) through the origin
      wall1=plane(X,origin).colored("Brown")
      wall2=plane(Y,origin).colored("Brown")
      tableTray=Cube(tableTrayDimensions).colored("ForestGreen")
      tableLeg1=Cube(tableLegDimensions).colored("ForestGreen")
      tableLeg2=tableLeg1.clone()
      tableLeg3=tableLeg1.clone()
      tableLeg4=tableLeg1.clone()

      # The next 2 lines correspond to the movement of tableLeg1 to the
      # corner of the tray  and to the bonding of the leg on the tray
      #################
      tableLeg1.against(tableTray,Z,Z,X,X,adjustEdges=-X-Y).glued_on(tableTray)
      tableLeg2.against(tableTray,Z,Z,X,X,adjustEdges=X+Y).glued_on(tableTray)
      tableLeg3.against(tableTray,Z,Z,X,X,adjustEdges=-X+Y).glued_on(tableTray)
      tableLeg4.against(tableTray,Z,Z,X,X,adjustEdges=X-Y).glued_on(tableTray)

      # The tray is moved and the legs follow because of the bonding 
      ################
      bottomOfTheLeg1=tableLeg1.point(0,0,0,"aap")
      tableTray.translate(origin-bottomOfTheLeg1) # vertical move: legs on the floor
      tableTray.translate(placementVector) # horizontal move

      # The flower pot is described as a difference between 2 cylinders then
      # placed on the table
      ################
      flowerPot=Cylinder(origin,origin+flowerPotHeight*Z,radius=flowerPotRadius).colored("Blue").glued_on(tableTray)
      toCut=Cylinder(origin+flowerPotThickness*Z,origin+2*flowerPotHeight*Z,radius=flowerPotRadius-flowerPotThickness)
      flowerPot.amputed_by(toCut)
      topCenterOfTable=tableTray.point(0.5,0.5,1,"ppp")
      flowerPot.translate(topCenterOfTable-origin)

      camera=Camera()
      camera.filmAllActors=False
      camera.location=origin+4*X+3.3*Y+1.5*Z
      camera.file="table.pov"
      camera.zoom(.315)
      camera.povraylights="light_source {<+4,4,4.8> color White " + "}\n\n"
      camera.lookAt=topCenterOfTable
      camera.actors=[ground,wall1,wall2,tableTray]
      camera.shoot
      camera.pov_to_png

    
..
   Faces of a box.
   --------------------------

   The above code requires some notation to be explained. 

   Starting from its center, an object admits 6 faces of dimension 2 
   denoted by X,-X,Y,-Y,Z,-Z which correspond to the colored facets
   in the above example. Remember that this refers to the local coordinate
   of the object,  they are not not parallel to the global frame of the
   3D space.

   Similarly, there are 12 edges, denoted by X+Y,X-Y,.... Y-Z. 

   And there are 8 corners denoted by X+Y+Z,....-X-Y-Z.

..
   Moving a box against an other box. 
   -------------------------------------------------------------

   When we move a box A against a box B, we must do two things: orientate 
   the box A so that the faces of A are parallel to the faces of B, then 
   we must choose the faces of contact ( putting A above or below B, on
   the left or on the right...)

   The command 

   ..  code-block:: python 

       A.against(B,faceA1,faceB1,faceA2,faceB2) 

   means that: 

   * the orientation of A is such that :

     * faceA1 and faceB1 are positivly parallel
     * faceA2 and faceB2 are positivly parallel

   * FaceA1 is the face of contact of A between A and B. 
   * The faces of A and B in contact have the same center

   For instance, in the following code, we take conventions of colors RGB
   for the axis XYZ. The instruction
   yellowCube.against(brownCube,-Z,Y,X,X) means that vectors -Z
   (opposite to the blue half-line) of the yellow cube is in the same
   direction that the Y ( green) of the Brown Cube. The face -Z of
   YellowCube is indeed a face of contact. And the two X axis (Red) are
   positivly parallel. 

   .. image:: ./docPictures/boxPlacementBasic.png

   ..
      .. code-block:: python

	 axisLength=0.8
	 axisThickness=0.06
	 arrowThickness=.3
	 brownCube=Cube(2,2,2) .colored("Brown")# the cube is moved above the plane
	 ground=brownCube.plane(Z,0,"a") .colored('Gray' )
	 yellowCube=Cube(1,1,1).colored("Yellow") # the cube is moved above the plane

	 xaxis=FrameAxis(brownCube.center,brownCube.center+7*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(brownCube)
	 yaxis=FrameAxis(brownCube.center,brownCube.center+7*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(brownCube)
	 zaxis=FrameAxis(brownCube.center,brownCube.center+7*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(brownCube)

	 xaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(yellowCube)
	 yaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(yellowCube)
	 zaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(yellowCube)

	 yellowCube.against(brownCube,-Z,Y,X,X)

	 camera=Camera()
	 camera.file="boxPlacementBasic.pov"
	 camera.location=origin-5*Y+4*Z-2*X
	 camera.filmAllActors=False
	 camera.actors=[ground,brownCube,yellowCube,xaxis,yaxis,zaxis,xaxisg,yaxisg,zaxisg] # what is seen by the camera   camera.lookAt=.5*(basket2+basket)
	 camera.zoom(.2512)
	 camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
	 camera.pov_to_png # show the photo, ie calls povray. 


   Suppose that we want to move the yellow cube to the left till the
   edges of both Cubes coincide. We need to push Yellow Cube in direction
   opposite to the red, ie. -X.  Thus we add the option
   ajustedges=-X ie we put    yellowCube.against(brownCube,-Z,Y,X,X,adjustEdges=-X)

   .. image:: ./docPictures/boxPlacementEdge.png

   ..
      .. code-block:: python

	 axisLength=0.8
	 axisThickness=0.06
	 arrowThickness=.3
	 brownCube=Cube(2,2,2) .colored("Brown")# the cube is moved above the plane
	 ground=brownCube.plane(Z,0,"a") .colored('Gray' )
	 yellowCube=Cube(1,1,1).colored("Yellow") # the cube is moved above the plane

	 xaxis=FrameAxis(brownCube.center,brownCube.center+7*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(brownCube)
	 yaxis=FrameAxis(brownCube.center,brownCube.center+7*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(brownCube)
	 zaxis=FrameAxis(brownCube.center,brownCube.center+7*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(brownCube)

	 xaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(yellowCube)
	 yaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(yellowCube)
	 zaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(yellowCube)

	 yellowCube.against(brownCube,-Z,Y,X,X,adjustEdges=-X)

	 camera=Camera()
	 camera.file="boxPlacementEdge.pov"
	 camera.location=origin-5*Y+4*Z-2*X
	 camera.filmAllActors=False
	 camera.actors=[ground,brownCube,yellowCube,xaxis,yaxis,zaxis,xaxisg,yaxisg,zaxisg] # what is seen by the camera   camera.lookAt=.5*(basket2+basket)
	 camera.zoom(.2512)
	 camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
	 camera.pov_to_png # show the photo, ie calls povray. 

   With yellowCube.against(brownCube,-Z,Y,X,X,adjustEdges=X+Y), the
   yellow Cube goes to the upper right. With,
   yellowCube.against(brownCube,-Z,Y,X,X,adjustEdges=0.8*(X+Y), it
   nearly goes to the upper right, as shown-below. 

   .. image:: ./docPictures/boxPlacementCorner.png

   ..
      .. code-block:: python
	 :hide:

	 axisLength=0.8
	 axisThickness=0.06
	 arrowThickness=.3
	 brownCube=Cube(2,2,2) .colored("Brown")# the cube is moved above the plane
	 ground=brownCube.plane(Z,0,"a") .colored('Gray' )
	 yellowCube=Cube(1,1,1).colored("Yellow") # the cube is moved above the plane

	 xaxis=FrameAxis(brownCube.center,brownCube.center+7*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(brownCube)
	 yaxis=FrameAxis(brownCube.center,brownCube.center+7*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(brownCube)
	 zaxis=FrameAxis(brownCube.center,brownCube.center+7*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(brownCube)

	 xaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(yellowCube)
	 yaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(yellowCube)
	 zaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(yellowCube)

	 yellowCube.against(brownCube,-Z,Y,X,X,adjustEdges=.8*(X+Y))

	 camera=Camera()
	 camera.file="boxPlacementCorner.pov"
	 camera.location=origin-5*Y+4*Z-2*X
	 camera.filmAllActors=False
	 camera.actors=[ground,brownCube,yellowCube,xaxis,yaxis,zaxis,xaxisg,yaxisg,zaxisg] # what is seen by the camera   camera.lookAt=.5*(basket2+basket)
	 camera.zoom(.3512)
	 camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
	 camera.show # show the photo, ie calls povray. 

   If we want to put the yellow cube off the brown cube, we can add an
   offset. The offset is in global coordinates. In our picture, the
   yellow cube has been rotated,  but the brown cube has not moved so its
   coordinates are still parallel to the global axis of the scene. Thus
   the offset must be a negative mutltiple of the green axis Y of the Brown
   Cube. For instance, we may put
   yellowCube.against(brownCube,-Z,Y,X,X,adjustEdges=.8*(X+Y),offset=-0.7*Y)

   .. image:: ./docPictures/boxOffset.png

   ..
      .. code-block:: python

	 axisLength=0.8
	 axisThickness=0.06
	 arrowThickness=.3
	 brownCube=Cube(2,2,2) .colored("Brown")# the cube is moved above the plane
	 ground=brownCube.plane(Z,0,"a") .colored('Gray' )
	 yellowCube=Cube(1,1,1).colored("Yellow") # the cube is moved above the plane

	 xaxis=FrameAxis(brownCube.center,brownCube.center+7*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(brownCube)
	 yaxis=FrameAxis(brownCube.center,brownCube.center+7*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(brownCube)
	 zaxis=FrameAxis(brownCube.center,brownCube.center+7*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(brownCube)

	 xaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(yellowCube)
	 yaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(yellowCube)
	 zaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(yellowCube)

	 yellowCube.against(brownCube,-Z,Y,X,X,adjustEdges=.8*(X+Y),offset=-.7*Y)

	 camera=Camera()
	 camera.file="boxOffset.pov"
	 camera.location=origin-5*Y+4*Z-2*X
	 camera.filmAllActors=False
	 camera.actors=[ground,brownCube,yellowCube,xaxis,yaxis,zaxis,xaxisg,yaxisg,zaxisg] # what is seen by the camera   camera.lookAt=.5*(basket2+basket)
	 camera.zoom(.3512)
	 camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
	 camera.show # show the photo, ie calls povray. 

   Finally, it is possible to add the option adjustAxis=[p1,p2]. The
   adjustement computed by Pycao is a move  parallel to the face of contact (in our case,
   the -Z face of YellowCube) so that p1 and
   p2 are on a line parallel to the blue axis of YellowCube.  To
   illustrate, this notion we make the corners of YellowCube and
   BrownCube coincide. 

   .. image:: ./docPictures/boxAdjustAxis.png

   .. code-block:: python

      axisLength=0.8
      axisThickness=0.06
      arrowThickness=.3
      brownCube=Cube(2,2,2) .colored("Brown")# the cube is moved above the plane
      ground=brownCube.plane(Z,0,"a") .colored('Gray' )
      yellowCube=Cube(1,1,1).colored("Yellow") # the cube is moved above the plane

      xaxis=FrameAxis(brownCube.center,brownCube.center+7*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(brownCube)
      yaxis=FrameAxis(brownCube.center,brownCube.center+7*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(brownCube)
      zaxis=FrameAxis(brownCube.center,brownCube.center+7*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(brownCube)

      xaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*X,axisLength,axisThickness,arrowThickness).colored('Red').glued_on(yellowCube)
      yaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Y,axisLength,axisThickness,arrowThickness).colored('Green').glued_on(yellowCube)
      zaxisg=FrameAxis(yellowCube.center,yellowCube.center+10*Z,axisLength,axisThickness,arrowThickness).colored('NavyBlue').glued_on(yellowCube)

      upperLeftBrownPoint=brownCube.point(0,0,1,"ppp")
      upperLeftYellowPoint=yellowCube.point(0,1,1,"ppp")
      yellowCube.against(brownCube,-Z,Y,X,X,adjustAxis=[upperLeftYellowPoint,upperLeftBrownPoint])

      camera=Camera()
      camera.file="boxAdjustAxis.pov"
      camera.location=origin-5*Y+4*Z-2*X
      camera.filmAllActors=False
      camera.actors=[ground,brownCube,yellowCube,xaxis,yaxis,zaxis,xaxisg,yaxisg,zaxisg] # what is seen by the camera   camera.lookAt=.5*(basket2+basket)
      camera.zoom(.3512)
      camera.shoot # takes the photo, ie. creates the povray file, and stores it in camera.file
      camera.show # show the photo, ie calls povray. 

..
   Relative placement: Above,behind,on_left_of...
   ------------------------------------------------------------

   Left, right, up are relative notions. The instruction
   *object1.above(object2,adjustEdges,offset)*
   is a synononym of *object1.against(object2,-Z,-Z,X,X,adjustEdges,offset)*

   To say the things differently, the instructs, above, behind, in_front_of
   .... suppose that we see the
   object from a point (0,-y,0) with y large enough, that the frame
   that we use is direct and that the gravity vector is (0,0,-g) in this
   frame. 
   
