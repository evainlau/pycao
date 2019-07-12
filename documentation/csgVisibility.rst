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


.. image:: ./docPictures/csgVisibility.png

.. code-block:: python 

    wall=Cube(2,2,2).colored("Brown").translate(origin-X-Y+.5*Z) # 

    cyl=Cylinder(start=origin,end=origin+5*Z,radius=0.5).colored('SpicyPink')

    axis=Segment(point(0,0,0),point(0,0,1))
    cyl2=ICylinder(axis,0.25).colored('Yellow') #an infinite cylinder 


    # Using amputations : corresponds to the yellow and pink marks since the elements amputed don't keep their textures
    cyl.amputed_by(cyl2,keepTexture=False)
    wall.amputed_by(cyl,keepTexture=False)

    # Using intersection : no change of colors since keepTexture is true by default.
    axis.translate(3,0,0)
    cyl3=ICylinder(axis,3.2).colored("Green")
    axis.translate(-6,0,0)
    cyl4=ICylinder(axis,3.5).rgbed(1,1,1)
    wall.intersected_by([cyl3,cyl4])
    wall.rotate(Segment(origin,Z),.5)





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
   A.intersect(tool)

