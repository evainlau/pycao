===========
Remarks
===========

We group here some random remarks that may help you to understand
the notations and their coherency. 


Aliases
--------
We have aliases to speed up the input and for readability.

.. code-block:: python

   X=vector(1,0,0)
   Y=vector(0,1,0)
   Z=vector(0,0,1)
   T=point(0,0,0)
   origin=point(0,0,0)
   plane=AffinePlaneWithEquation
   line=Segment

In principle, the constructors of objects start with a capital
letter (MassPoint,Cone,Cylinder,Cube...). This is the standard convention 
for Python classes. However, for the objects we use so much, we 
have inserted alias with or without capital letter so that both are usable
(origin or Origin,point or Point,vector or Vector,line or Line,plane
or Plane). 


Maps and vectors
-----------------
When an affine map is applied to a vector, it is the underlying linear
map which is applied, as this is the operation which makes sense
mathematically. For instance, a vector remains unchanged if a
translation is applied (Intuitivly, the two extremal points of the
vectors are moved, thus the vector joining these two points remains
unchanged). 
