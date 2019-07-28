********************
CSG 
********************
The basic operations of constructive solid geometry (CSG in short)
are union, intersection, difference. 

Union
------
We have already seen how to make a compound object. This corresponds
to the union and you can use it in CSG constructions. 


Intersection and difference
----------------------------

The difference of A and B is defined by *amputed_by*. 
The intersection is defined by *intersected_by*
Note that the cutting shape may mark the amputed object with its color
depending on the options. 

By default, when A is cut by B, B is glued on A so that when you move
A , the hole that you made will not move relativly to A (a hole in the
center remains in the center for instance).  


.. image:: ./generatedImages/csg.png


.. literalinclude:: csg.py
   :start-after: bbloc1
   :end-before: ebloc1






In the above, we put 

.. code-block:: python 

   camera.filmAllActors=True

Nevertheless, the cylinders used to cut the cube do not appear. The
reason is that the tool used to cut is declared invisible. By default,
in A.amputed_by(B), B is not seen, does not follow when A is moved,
does not impose its texture/color

The general syntax with the possible options is: 

.. code-block:: python 
    
    A.intersected_by(cuttingShape,throwShapeAway=True,keepTexture=True,takeCopy=False,glued=True)
    A.amputed_by(cuttingShape,throwShapeAway=True,keepTexture=True,takeCopy=False,glued=True):

The intersection and difference is not recursive, ie. does not include
the children. To intersect A with B and its children:

.. code-block:: python
		
   for tool in B.descendants_and_myself():
     A.intersected_by(tool)

