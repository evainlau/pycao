**************************
Genealogy and Compounds
**************************

Now, you are able to position objects individually. However, usually,
you need to move the objects in groups, like a watch which moves with
the arm of a person or like all the parts of your bike when you move
the bike.

In pycao, there are two ways to aggregate the objects:
a genealogy relationship parent/childre or a compound aggregate. 
In this note, we shall learn the basics of 
the two different notions and compare them. 

Genealogy
-----------------

Here is a small construction of a colored Cube a la  Rubik.

.. image:: ./generatedImages/genealogyAndCompounds1.png


.. literalinclude:: genealogyAndCompounds1.py
   :start-after: bbloc1
   :end-before: ebloc1

   
Thus we see that
the declaration 

.. code-block:: python
    	      
              d.glued_on(basket)

made d a child of  basket. An object may have  many children but only
one parent. When the parent moves, the child follows (and recursivly,
the grand child follows if it exists, and so on...)
In our Rubik's cube situation, we have moved the basket,
and the 27 cubes followed because they were glued on the basket, they
are children.

However, when the children move, the parent stays fixed. Thus this is
an asymetric relation. 


Cameras and the genealogy system
---------------------------------------------------------------


In the line camera.actors, we put:

.. code-block:: python

   camera.actors=[ground,basket,basket2]
   
There is no mention the 27 small cubes : only the containing basket. Since cubes are children 
of the basket, they are seen by the camera if the basket is seen. 
If any, the camera will include automatically the children, 
the children of the children... in the photo. 

Finally, remark that when an object is copied, all its children are
copied too (and recursivly, the children of the children... )

Compounds
--------------------------

The parent/children realtion is asymetric. The Compound notion
brings object together in aymmetric way. It is called as

.. code-block:: python

       Compound (slavesList=[o1,o2,...])

Each entry of  slavesList is

- an object in World with no genealogy
- or a sublist [name,objectInworld], where name is a string. 

In the second case, the subobject will be accessible with self.name

Here is an example where we access to the cylinder subpart to
put it in a vertical position.
Moreover, we see that the color applied to the
compound overwrites the colors of the components ( the
individual colors of  the components remain if we don't overwrite).

.. image:: ./generatedImages/genealogyAndCompounds2.png


.. literalinclude:: genealogyAndCompounds2.py
   :start-after: bbloc1
   :end-before: ebloc1



Genealogy versus Compound
-------------------------------------------------------------

	
When a compound is moved, all the objects in the slavesList are moved
simultaneously, thus this is symmetric. Moreover, a color on the
compound is affected to each object, thus the compound really
behaves like a unique object. In particular, when you intersect
with a compound, you intersect with all objects in the compound. 

A compound is is a less granular notion than a genealogy
relationship. If you often use subcomponents ( to intersect for
instance. or for coloring), it is more convenient with
parent/children. If you often use the components as whole object,  a compound
is preferable. For small projects, using only parent/children
gives quick access to the objects. 
For large projects, the notation
compound1.subcompoundname.componentName
avoids a collision of the names of the objects.
This is in particular very useful to build libraries
since the names of the parts of the objects imported
from different libraries will not collide. 

Technically, there are conditions to use the notions
of genealogy and compound simultaneaously.
Be careful that it is
not allowed is to give a filiations between two elements of the same
compound. If you do so,  the child moves twice when you move the compound,
once as an element of the compound, once as a child, and the movement
gives unpredictable results. 

	
If o is an object, o.clone() makes a recursive copy including the
children, but neither the parent or the compounds containing it. 
