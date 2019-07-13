====================
Rotating objects
====================
Syntax
--------
As for translations, the rotations use implicitly the data
attached to the objects, axis or hook when needed.
And the high-level rotations are defined withs geometirc
goals (parallelism, objective to put points on a common plane... )
and the angles are automatically computed in
the background with no math computations on your shoulders.

We start with the code and the illustrating examples follow. 

.. code-block:: python

   c.parallel_to(other,fixed=None) 		
   c.grotate(ax,o1,o2) 		
   c.self_grotate(o2)

The first instruction moves c so that it becomes parallel to (the
selected axis of) other,
where other is an object with an axis or a vector. If fixed  is given this is a fixed
point of the transformation where fixed is a point or an object with a hook.

The second instruction rotates c around the axis ax or around
ax.axis() if ax is an object. O1 and O2 are points or objects with
hooks. The angle of rotation M is the amount such that o1 and o2 would be
"at the same level" in a race around the axis, to be precise such that M(o1) and o2 are on a
common plane passing through the axis. The example will clarify. 

The last instruction does the same thing as the second instruction 
but some data is implicit:  ax=c.axis() and o1=c.hook().

Illustration
--------------

In the following illustration, we have defined a simple clock with
adequate hooks and axis.


.. literalinclude:: rotations.py
   :start-after: bbloc1
   :end-before: ebloc1


.. image::  ./docPictures/rotations1.png

.. image::  ./docPictures/rotations2.png

.. image::  ./docPictures/rotations3.png

.. image::  ./docPictures/rotations4.png
		
