******************************************************************************************************
Technical documentation for developpers or advanced users: short version
******************************************************************************************************

The objectsIn World  of pycao
------------------------------
There is a class objectsInWorld which contains all the 
objects that can be embedded in 3D : camera, points, line, massic points...
These objects can be manipulated through the methods move_alone
(without children) and move (with children). 

To move an object, the computations are not always done in the same
way and they depend on the type of ObjectInWorld we have, 
Technically, OIW contains three subclasses:
- Primitive
- Elaborate
- Compound


The primitive objects are "simple" objects. When they move, information on them is known
and computed in real time, in a direct way.


The elaborate objects are generally objects of medium complexity. When
they move, the computation is postponed. information on them is known indirectly through a matrix
self.mapFromParts which keeps track of the movement. Objects go in
this class when this is more economical in terms of computation to 
store the matrix of movement thant to compute everything, or when 
this is not possible to make the computations on the parameters
because the class is not stable by non orthogonal transfomations. 


The compound class contains objects which are union of primitive,
elaborate or previously defined compound instances, called slaves 
of the compound. The children of the slaves are part of the object
(to insure that drilled object remain drilled in the compound).
or equivalently, compound is a list of branches gathered in 
a single node. 

The master of the compound is empty. Move_alone 
on a compound performs a move_alone on the master (ie changes 
self.mapFromParts and a move 
(not move_alone, as children are in the compound)
on each slave in the union. 
There are no genealogy relations between the master and the slaves
to ensure that the method move does not move the slave twice. 
The texture applied to the slaves is taken from the master 
if the slave itself has no texture. 

The compound class is a class
which is useful to build librarys : derive from this class, 
and use the parameters in the init function to build the object. 
Then we obtain a new object, parametrizable, considered as a unique 
object by the software. 

The formalism of this class is such that 
all the meaningful information about the objects ie. markers
principally survive in this construction. 

Markers
---------
To avoid carrying unnecessary information on the objects, like for the
center of cube, we store it as a method which can be applied to an
instance. Tecnically a marker myClass.markername() is a callable attribute of the class
such that self.markername() returns self.markers.markername.move(self.markersMatrix)

Since only elaborate and compound objects have a self.mapFromParts non
trivial, only elaborate and compound have markers.


Elaborate, primitive, compounds Objects: how they are implemented
------------------------------------------------------------------
Let's sum up the above discussion in terms of implementation

*  Primitive instances self are
   *  computed in real time, ie. recomputed each time the object is
   moved.
   * have no markers.
   * have a meaningless map self.mapFromParts (always identity)

* Elaborate instances
  * has an attribute self.parts
  * have an attribute self.mapFromParts
  * has attributes self.markers.markerName with corresponding attribute self.makerName() which returns the marker in real time.
  * The raytracer is able to draw a picture using self.parts and self.mapFromParts
  * The init-function ends with self.markers_as_functions()


* Compound instances
  * have an attribute self.slaves which is a list where each entry is
    an OIW or a couple ["name", OIW]. In the second case, the slave 
    can be accessed after the construction through the master m with the calling sequence
    m.name 
  * Self.slaves is useful as an input method but self.csgSlaves
    is the list which is really useful for drawing. 
  * have an attribute self.mapFromParts
  * has attributes self.markers.markerName with corresponding
    attribute self.makerName() which returns the marker in real time
    using the map of the master
  * The raytracer draw each slave individually
  * The init-function ends with self.markers_as_functions() and self.build_from_slaves()


