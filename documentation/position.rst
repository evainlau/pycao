****************************************
Positionning the Objects (translations)
****************************************

Hooks
--------

The paradigm used to translate an object is that of hooks.
A hook is like a mark done on a piece of wood by a carpenter. This
mark will move with the object and you can use it as a reference for
your future work.  The good point with hooks is that 
we talk about geometric points on the objects and they make sense
whatever the position of the object in the global space. 

Let's go to practice. We show how
to put a cube on top of an other cube using hooks. 

.. code-block:: python

   redCube=Cube(2,4,6).colored("Red")
   redCube.add_hook("top",point(1,2,6)) # usually done at creation time when the coordinates are easy to understand
   redCube.add_hook("center",point(1,2,3)) # an other hook. The active hook of redCube is "center" as it is created. The previous hook "top" is still known but not selected. 
   redCube.hooked_on(point(2.2223,3.5672,4.345)) # moves the hook "center" to a random destination point and the cube follows
   greenCube=Cube(1,2,3).colored("Green") 
   greenCube.add_hook("bottom",point(.5,1,0))
   redCube.select_hook("top") # we change the active hook
   greenCube.hooked_on(redCube) # sends the active hook "bottom" of greenCube to the active hook "top" of redCube

   
The important point here is that we have postionned the greenCube
without using the global coordinates of the redCube. In particular,
you can change the random coordinates of the fourth line,
the following will remain OK  and the green cube will stay on top of the red one. This is
because the hook is a coordinate free approach and this makes your
code robust and easy to maintain. 

Note in the above example that the syntax takes 2 forms:

.. code-block:: python

   object.hooked_on(point)
   object2.hooked_on(object1)

.. image:: ./docPictures/positionWithHooks.png

More markers and translations
--------------------------------

Sometimes, you want to put a marker on your object which is a line
rather than a point. A typical example is when you want to open a
drawer : you translate the drawer along a prescribed line attached to
the drawer.

To move your drawer, you have the fonction self_translate. You
first add the marker to your object. Then self_translate makes a translation
along the vector attached to the object. If you move the object, the
marker will move with the object and you keep the same code to open
your drawer. 

Here is the code and the
images. 

.. code-block:: python
		
    # def of the drawer switched"
    yellowDrawer.add_axis("axis",line(origin,origin+Y)) #The vector of the axis is v=Y
    camera.file="drawerClosed.pov"
    camera.shoot
    yellowDrawer.self_translate(-.1) # moves by -.1*v=-.1*Y
    camera.file="drawerOpen.pov"
    camera.shoot

.. image:: ./docPictures/drawerClosed.png

.. image:: ./docPictures/drawerOpen.png




Finally, you can use the translations with goals, hence the names
gtranslate and self_gtranslate. Typically used on a race, you want to
move a runner till he arrives at the same level of an other runner. 
Or for instance when we want to fully open the previous drawer and
stop exactly at the moment the drawer is outside the box.

.. code-block:: python
		
    yellowDrawer.select_hook("back") # A point in the back of the drawer
    greenBox.select_hook("front") # A point in the front of the greenBox
    yellowDrawer.self_gtranslate(greenBox)

.. image:: ./docPictures/drawerFullOpen.png

The syntax is
	   
.. code-block:: python

   c.gtranslate(vec,start,goal) 
   c.self_gtranslate(self,goal) #    

The first instruction translates c along a translation t   with vector
v such that  t(start),goal are in a common plane   orthogonal
to v. Start and  goal are  possibly a point or an obect with an active hook.

The second instruction does the same thing using implicitly vec=c.axis() and start=c.hook()
