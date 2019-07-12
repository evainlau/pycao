
********
Cameras
********

The actors
------------------

The 3d-view is completly defined from our camera.
The lights, zoom, orientation of the space, which actors are seen
by the camera ,etc , more generally
every element of the 3D-view depends of the camera. 
The main options of the cameras can be changed in the template files.
In particular, we may define multiple cameras, for instance camera1 and camera2, each one looking from
a specific position and/or regarding different objects in the scene.


Choosing which objects are seen by the camera is quite common
to focus on one group of objects. This is the variable
camera.actors which controls what is seen by the camera.
On the photo taken by camera.shoot, you will see
the members of camera.actors and, recursivly,
all the children of the actors. 

For instance,, if you want to see just 2 objects object1,object2 and their children,
you set camera.filmAllActors=False and you declare
camera.actors=[object1,object2]

If you want to see everything, you may be helpled by the declaration
camera.filmAllActors=True.
This will add to your camera.actors list all the objects constructed.


Visibility
---------------------

Usually, the camera.actors list allows a good control. 
But if the control using camera.actors is not granulated enough,
(for instance if you want to include an object but not its children),
you can get a better control with the visibility arguments.

Each objects has a visibility and
the cameral has a visibility level : which
can be set with: 

.. code-block:: python 

    object.visibility=number # 1 by default
    object.booleanVisibility=number # 1 by default
    camera.visibilityLevel=number # 1 by default

We recommand by convention to let the visibility level between 0
and 1 so that object imported from elsewhere will be seen if
visibility=1 and wont' be seen if visibility<0. 

More precisely, an object which is not included in a union, intersection, or
difference is visible if its visibility is at least the visibility of the
camera. An object in a union behaves like an object alone.

..
   For an object A-B, ie of the form A.amputed_by(B) or
   A.intersected_by(B), sometimes we want to see for checking only A, or
   or A-B, independently of the visibility of the tool B used to cut A.  
   To allow this level of detail in the rendering,  we introduce the booleanVisibility
   attribute. 

For a difference A-B, what is seen by the camera is

*  nothing is visibility(A)<camera.visibilityLevel
*  A if  visibility(A)>=camera.visibilityLevel and  booleanVisibility(B)<camera.visibilityLevel
*  the difference A-B if  visibility(A)>=camera.visibilityLevel and  booleanVisibility(B)>=camera.visibilityLevel

..   
   In this last case, a fullcopy of B is computed, adobted by A,  and A is replaced by
   A-fullcopy(B).

