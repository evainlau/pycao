Maths
=========

The preceding paradigms have tried to take off you the pressure of
math computations. If however, you need to do the maths by yourself,
here are the tools.

Linear and affine maps
----------------------------------

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
(X,Y,Z) to (X,X+Y,Z). 


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

Rotations

..code-block:: python

Rotations
--------------

.. code-block:: python
		
   mathutils.Map.rotational_difference(start,goal)  

 is the linear rotation sending the vector start to the vector goal

.. code-block:: python

   axis=line(point1,point2)
   c.rotate(axis,angleInRadians)

for a simple rotaion in radian. If you want to use
the axis selected for the object implicitly: 
   
.. code-block:: python

   c.self_rotate(angle):

Rotations with multiple of math.pi implicit if you are tired to
typeset math.pi. 	
.. code-block:: python	

   def self_pirotate(self,angle):
        return self.rotate(self.axis(),math.pi*angle)

A rotation in degrees	
.. code-block:: python			
	
    def self_degrotate(self,angle):
        return self.rotate(self.axis(),math.pi*angle/90)




Shorticuts
-------------------

Shortcuts for scaling or for inverting axes:

.. code-block:: python

   c.scale(a,b,c) #shortcut for c.move(Map.linear(a*X,b*Y,c*Z))

   def flipXY(self):
		return self.move(Map.linear(Y,X,Z))

   def flipXZ(self):
		return self.move(Map.linear(Z,Y,X))

   def flipYZ(self):
		return self.move(Map.linear(X,Z,Y))

   def flipX(self):
		return self.move(Map.linear(-X,Y,Z))

   def flipY(self):
		return self.move(Map.linear(X,-Y,Z))

   def flipZ(self):
		return self.move(Map.linear(X,Y,-Z))
   
