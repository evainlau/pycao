Maths
=========

The preceding paradigms have tried to take off you the pressure of
math computations. If however, you need to do the maths by yourself,
here are the tools.

Maths
---------

To make a translation of vector v=Vector(x,y,z) or a rotation

.. code-block:: python

   c.translate(v)
   axis=line(point1,point2)
   c.rotate(axis,angle)
   
It is possible to use 
a general map M. 
For instance:

.. code-block:: python

   M=Map.linear(X,X+Y,Z)
   c.move(M)

moves the object c by the linear map M sending the canonical base 
(X,Y,Z) to (X,X+Y,Z). A shortcut for c.move(Map.linear(a*X,b*Y,c*Z))
is

.. code-block:: python

   c.scale(a,b,c)




Using linear maps and translation, we can 
describe any affine map. The syntax is 

.. code-block:: python

   M=Map.affine(a,b,c,w)
   c.move(M)
which is equivalent to 

.. code-block:: python

   M=Map.linear(a,b,c)
   N=Map.translation(w)
   c.move(N*M)
