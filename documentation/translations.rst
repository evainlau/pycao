****************************************
Translating Objects
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


.. literalinclude:: translations1.py
   :start-after: bbloc1
   :end-before: ebloc1


   
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

.. image:: ./generatedImages/translations1.png

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

.. literalinclude:: translations2.py
   :start-after: bbloc1
   :end-before: ebloc1


.. image:: ./generatedImages/translations21.png

.. image:: ./generatedImages/translations22.png




Finally, you can use the translations with goals, hence the names
gtranslate and self_gtranslate. Typically used on a race, you want to
move a runner till he arrives at the same level of an other runner. 
Or for instance when we want to fully open the previous drawer and
stop exactly at the moment the drawer is outside the box.


.. literalinclude:: translations2.py
   :start-after: bbloc2
   :end-before: ebloc2


.. image:: ./generatedImages/translations23.png

The syntax is
	   
.. code-block:: python

   c.gtranslate(vec,start,goal) 
   c.self_gtranslate(self,goal) #    

The first instruction translates c along a translation t   with vector
v such that  t(start),goal are in a common plane   orthogonal
to v. Start and  goal are  possibly a point or an obect with an active hook.

The second instruction does the same thing using implicitly vec=c.axis() and start=c.hook()
