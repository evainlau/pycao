********************************************************
Find one's way in space: notations for the positions
********************************************************

The first thing that we need is to be able to define precisely the
points that we want to put our objects at the required position. 

Notations for points, vectors and barycenters
------------------------------------------------

A point p  in space may be defined by the following expressions:

.. code-block:: python
		
   p=point(3,4,6)
   p=origin+3*X+4*Y+6*Z
   p=0.5*origin+0.5*point(6,8,12) # p is in the middle between origin and point(6,8,12)

A vector may defined by the following expressions:
		
.. code-block:: python
		
   v=Vector(3,4,6)
   v=3*X+4*Y+6*Z # a linear combination of vector is a vector
   v=0.5*(point(6,8,12)-origin) # a difference between 2 points is a vector


The barycenter is a math notion generalizing the center :
It makes sense to take linear combinations of 
points as long as the sum of coefficients is 1: this is a barycenter.
The following code defines a center, and the barycenters of the points p1,p2,p3,p4 with
coefficients n1=.2,n2=.3,n3=..4,n4=.1 which makes sense since n1+n2+n3+n4==1


.. code-block:: python

    center=0.5*p1+0.5*p2
    n1=.2,n2=.3,n3=..4,n4=.1
    barycenter=n1*p1+n2*p2+n3*p3+n4*p4 
   
Recall that in contrast, in maths it is not allowed to add 2 points : this makes no sense. 
In pycao, you can do it but we encourage you not to do it ( the output
is a massic point of mass 2 in an abstract massic space, neither a point
(mass 1) nor a vector (mass 0)). You can check by yourself

.. code-block:: python

   print(origin+origin)
   >>Mass Point  [0 0 0 2]

Remark: in the notation, point(x,y,z), the coordinates (x,y,z) are
global coordinates. This is not to be confused with the notation
object.point(x,y,z) that we will explain later, and where coordiantes
are relative to the object. 
   
Reminder on points and Vectors
----------------------------------

For those who have forgotten the maths, here are some rule of thumbs
as a reminder for notions of points and vectors, 

Usually, points and vectors are displayed picturally as follows. 


.. image:: ./docPictures/pointsAndVectors.png


Recall that we have the formulas :


.. math::
   
   point+vector=point

   point-point=vector

   vector+vector=vector



In the above picture, we have:

.. math::

   yellow point+blueVector=orangePoint

   redPoint-orangePoint=GreenVector

   blueVector+greenVector=redPoint-yellowPoint

This formalism of points and vectors is known to pycao. 




