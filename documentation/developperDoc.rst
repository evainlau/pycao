**********************************************************************
Technical documentation for developpers or advanced users
**********************************************************************


The objectsIn World  of pycao
------------------------------
There is a class objectsInWorld which contains all the 
objects that can be embedded in 3D : camera, points, line, vectors...
Formally, an instance of ObjectInWorld is an object on which 
we can operate using an instance of the class Map. 

More informally, the class objectInWorld is created to share 
methods between many different kind of objects. For instance, 
whatever the object self is, camera or line, it is moved 
using the declaration self.move(map). 

In practice, there are classes
which derive from ObjectInWorld, for instance Line,Plane,Camera...
The objects that we use are instances of these derived classes.
There is no pure instance of ObjectInWorld, only instances of derived classes.


Moving the objects and the genealogy system
---------------------------------------------

Every object self instance of ObjectInWorld can be nested in a genealogy system, 
with one parent self.parent, and a list of children self.children. The
method move moves self with all its children. The method move_alone, 
move self without its children, and is called recursivly in move. 

Move is the fundamental method to move any object. The advised 
procedure is the following. The user defines a map M  
using any of the possible primitives in the class mathutils.Map. Then
applies on self with the instruction self.move(M).

For  very common displacements: translation, rotation,
scale, there are shortcuts. 
Instead of applying M=Map.translation(v), self.move(M) 
the user may directly type self.translate(v). This is compatible 
with the recommanded procedure since translate, rotate 
and scale are basically macros applying the procedure. 
 
THe function move returns self, so that the operations 
may be nested self.move(M1).move(M2). However, Remark  it is faster to
compute self.move(M1*M2). With  n children (n+1 operations) against 
2n operations. Thus the chaining is useful only when the definition of 
M2 requires parameters obtained after the displacement of M1, or with 
few children.




Decomposable and primitive Objects: why we need them
---------------------------------------------------------

Instances of ObjectInWorld can be divided using two classifications:
An object may be :
- decomposable or indecomposable
- primitive/elaborate/compound. 



These distinctions are  motivated by performance consideration 
and ease of building library of objects, as we shall see. 


The decomposable objects  are built from several parts, for
instance when a line is built from 2 points. In contrast, 
some objects are "indecomposable" objects, like a point or a plane, 
and cannot be defined by simpler parts. This vocabulary 
is useful to understand the following, but is not 
implemented formally in the language. 


In contrast, the second classification primitive/elaborate/compound
is implemented. Theses concepts correspond to three classes
Primitive/Elaborate/Compound inheriting 
from ObjectInWorld. An object is primitive/elaborate/compound 
if it is an instance of the corresponding classes. 

Before the introduction of compound objects, we focus 
on the difference between primitive and elaborate. 
So for the moment, we discuss only the distinction between 
primitive and elaborate objects. 

Primitive objects are "simple", in a naive sense, ie. 
built from few indecomposable objects, 
Elaborate objects are in general more complex, built from many parts. 
There are different possibilities to
move an object, and the efficiency of the method 
depends on the complexity of the objects, 


To understand why the way we move objects depends on the
complexity of the object, consider the example of a convex envolop of n points p1,...pn 
that we move with maps M1,...Mk. There are 2 possibilities to make the
computation. First compute the composition M=Mk...M1, then compute 
Mp1,...,Mpn. The other possibility is to compute M1p1,...,M1pn,
M2M1p1...M2M1pn,,,,,Mk...M1p1, ...Mk..M1pn. Since in our model (see below)
evaluation requires 4 multiplication and composition 16
multiplications, in the first case, one needs 16(k-1)+4n
multiplications. In the second case, one nees 4nk multiplication.
Thus, when n<=4 the second method is faster 
and when n>4, the first method is faster. We could have done more precise
computations including additions, but what is important is the general 
picture : when the objects are simple, it is more rapid to 
do the computations at each step, and when the objects are complicated 
and carry a lot of information, like for a polygon with a lot of
points, a better option is to only 
remember the maps used to move the objects, without moving the object 
effectivly, and to perform the actual 
computations only at the end, at the level of the raytracer.
For these objects, we transmit to the
raytracer the indecomposable the parts at the time the object 
was created along with the matrix M=Mk...M1 used to move the object. 

We shall call the simple objects for which we do
the computations directly "primitive objects". The 
objects for which we only compute the matrix M and send it to 
the raytracer are called "elaborate" objects. Elaborate 
objects are in general assembled from many elements.

Formally, they are distinguished by the way the method self.move_alone is defined.
In the class Elaborate, we implements a method move_alone 
which basically computes the matrix M before sending it to 
the raytracer. For primitive objects,
move_alone is defined specifically for each object, it is not a
generic method of a class.  


An other element comes into the scene. Some objects are simple, 
but we need to declare them as "elaborate" objects since 
a direct calculation for them is not possible. 
Consider a line L defined by two points p1,p2. It is a primitive 
object, and M(L) is the line through M(p1),M(p2). Thus, to move 
L, we plainly move its parts. Suppose now that we want to apply the same 
strategy to a a portion of bounded cylinder,  
simply called "cylinder" in several raytracers.
There are two faces of this cylinder which are disks and the cylinder is 
defined by 3 "parts" p1,p2,R: one center for each disk and one radius.
One could try to move C by moving its parts and say that 
M(C) is defined by M(p1),M(p2) and R. However it is true only if M 
is an orthogonal transformation: The orthogonality between the 
disks and the axis of revolution is not preserved by a general map M. 
Thus for a cylinder, we shall transmit the initial points p1,p2, and R 
and M to the raytracer, even if it is defined by simple data: it is an elaborate object.


In general, the conclusion of the above discussion is that an object
is necessarily elaborate if it is an instance of a class 
which is not stable by affine transformation.
This includes cylinders, cubes... 
Since the primitive objects  must be simple and stable by affine
transformations: we
finally end up with a small list: points,vectors,lines,planes,conics and quadrics... 


Remark how the classifications decomposable/indecomposable and 
primitive/elaborate interact. Indecomposable objects, like points or planes, are always
primitive. Decomposable objects can be primitive (ex: lines  through two
points) or elaborate (ex: cylinder). 


Markers
--------

Very often, we need to access to some partial information in the
object. For instance, if we have drawn a lock, we need to know
the axis of the lock to put the key in the lock at the right
position. The lock is an elaborate object, thus the geometrical
information is not updated.

The workaround is the following. When an elaborate object is defined,
some markers may be put on it, like the axis above which could be a
marker called lock.holeAxis.  The markers are
transformed into functions at time creation of the elaborate object
with the same name. If we call lock.holeAxis 
then the position of the Axis is recomputed and a copy
of the Axis is returned to the user.

At the moment, a @property decorator is added but
this is a bad idea since this makes the confusion
between parts of the object and copies of these parts.
The correct terminology will be:
myObject.attribute= an object which modifies the shape of myObject if
the value is changed
myObject.attribute()=a copy that I can change freely without
perturbing myObject. 
This simple rule is easy to remember without diving in the subtilities
of elaborate/primitive objects. 

To sum up, the marker is a mechanism which allows
to do the intermediated computations only on the
elements we need and when we need them. Thus this preserves
time. Since we want to compute 
the coordinates of the marker, we want them to be primitive objects. 


Primitive objects do not have markers. If we need some information, we
simply add it in the definition of the primitive objects. 

Technical implementation of the Markers
-----------------------------------------

In the init function of the elaborate object:

.. code-block:: python 

        #self.markers. 
        self.markers=Object() #declares an object to store the markers
        self.markers.nameOfMyMarker1=thePrimitiveObjectUsedAsAMarker1
	self.markers.nameOfMyMarker2=thePrimitiveObjectUsedAsAMarker2 
        self.markers_as_functions() 

For each attribute markerName of self.markers,
the instruction    self.markers_as_functions().
builds a callable attribute  self.markerName
such that self.markerName() returns
self.markers.markerName.clone().move_alone(self.mapFromParts). 

The markers are not implemented efficiently. There is one instance of
the method self.markername() for each instance self whereas
it could probably be implemented as a class function
using some metaclass trick. 





Elaborate and primitive Objects: how they are implemented
------------------------------------------------------------------
Let's sum up the above discussion in terms of implementation

*  Primitive instances self are simple objects defined by a list of 
   indecomposable components which are attributes of self which are 
   computed in real time, ie. recomputed each time the object is moved. 
   Elaborate instances have an attribute self.parts which is a list of 
   indecomposable elements at the time of creation and a map self.mapFromParts.
* The raytracer is able to draw a picture using:

  * The attributes of a Primitive self
  * The list self.parts and the map self.mapFromParts for an Elaborate self
* The primitive objects are basic mathematical objects 
  and they are defined in the file mathutils. The elaborate 
  objects are defined in the file elaborate.py
* Every class of a primitive object is stable by affine transformations
* The rule to move an object self with the map M depends of the type
  of self:

  * If self is primitive, self.move_alone(M).attribute is defined
    specifically in self.__class__
  * If self is elaborate,  in self.move_alone(M), we do 
    self.mapFromParts=theMapUsedToMoveSelf*self.mapFromParts

At the moment, even primitive objects have an attribute
self.mapFromParts, which is not significant (its value is identity)
and this attribute is probably devoted to
disappear in the future. 


For elaborate objects, the attribute self.parts is 
a data at the time of creation and it is not intended to be accessed directy by the
user because it could harm. For instance, if a single corner of a cube is adopted
by a parent, moving the parent  will yield a mess in the cube. 
The access to different 
elements is via the marker mechanism. 


It is very important that this stuff remains transparent for the user of the
modeler. We need to check that every operation is accessible
in a unified methodology for primitive,elaborate and compound. 
Any evolution of the language has to keep this remark in mind. 


Rendering Objects
-----------------
The rendering is completly defined by a camera : what are the objects
seen or not seen, what lights are useful, what file are used for the
rendering, the  pre-hooks or post-hooks to be applied ... All these 
informations are defined as attributes of the camera. 

This gives the possibility to describe the scene completly. Then using 
several cameras, we get different views from different points. Each
camera may show only part of the scene to view clearly 
some details, with different lights if necessary. 

Remark that the orientation of the world depends on the camera 
(camera.directFrame=False by default) because it depends on the 
image rendered (an symmetry in a mirror changes the orientation)
whereas the conventions for orientation are governed by a global 
variable ( screwPositiveRotations=True by default).

The camera carries a visibilityLevel between 0 and 1. 
All objects whose visibility is at least the visibility 
of the camera are seen. Objects with visibility smaller 
than the visibilityLevel of the camera are not seen. 


The rendering in py2pov is done in several steps: 

* self.modifier() computes the modifier of the object ( no image and
  no shadow,no_reflection if insufficient visibility, texture) 
* self.object_string_but_csg() computes the object, forgetting the csg
  operations that apply on it.  
* self.object_string_alone computes the object, including csg
* self.object_string_recursive computes the objects, and all its
  child recursivly

  
For camera.filmAllActors=true, we did the following convention. If an
element is in a compound, then its parent is the compound. Thus, when
we list the actors, we don't include them as they will be
automatically included when we treat the compound and we don't want to
treat them twice. Althoug, when we deepcopy, we exclude the parents
of this deepcopy otherwise the whole stuff is recomputed. 



  
CSG generalities
-----------------

There are some reasons to consider the union on one side
(corresponding to the compound class in Pycao), and 
intersection and difference on the other side in very different 
ways, also the mathematical operations seem similar. 
Differences include copy issues, compatibilities with the genealogy system and 
with the visibility constants. 


Taking copies or not in CSG (This section outdated)
---------------------------------------------------------


Suppose we make a hole in an object A using an intersection with B. when 
we move A, we expect the hole to stay in the same position relatively 
to A, ie the hole follows A, even when B does not move. Similarly, 
if we move B alone, we don't want the hole to move in A, as it would
be very different from our habits in the usual world : when we move a
tool used to make a hole, the hole stays.
This means that we  need to construct A-copyOfB where copyOfB is
adopted by A when the input is A-B. 

Taking the copy to build difference also has a virtue: we avoid circular
dependencies in the boolean constructions. Blender 
refuses to take B a parent of A when constructing A-B. We have 
no problem with that because of the copy : even if B is a parent of A,
the copy of B is defined to be a child of A. 


For a union, this is different. A union is not 
really a new object, it is just some abstract logic to consider 
separate elements as a unique entity. 
If a queen is on a chess board, and 
if A=Q U B is the union of the queen Q and the board B, if we move the
queen and ask for a picture of the union A, we expect that the queen 
has moved on the board. For this reason, we don't want to take a copy 
of the components for a union. 

CSG and visibility
------------------
For the visibility and the union it is easy : an element in the union 
is visible if its visibility is at least the visibility of the
camera. 

For an object A-B, sometimes we want to see for checking only A, or
or A-B, independently of the visibility of the tool B used to cut A.  
To allow this level of detail in the rendering,  we introduce the booleanVisibility
attribute. 

For a difference A-B, what is seen by the camera is
- nothing is visibility(A)<camera.visibilityLevel
- A if  visibility(A)>camera.visibilityLevel and  booleanVisibility(B)<camera.visibilityLevel
- the difference A-B if  visibility(A)>camera.visibilityLevel and  booleanVisibility(B)>camera.visibilityLevel
In this last case, a fullcopy of B is computed, glued on A,  and A is replaced by
A-fullcopy(B).

The intersecection and the difference are handled similarly
because of the formula A cap B = A - (complementary of B). 

CSG and slave terminology
--------------------------

In this context, when we define A-[B,C], we say that A is the master 
and that B and C are the slaves of A.   

For a union, there are only 
slaves, and no master, to respect the symmetry of the union. 

CSG and compatibility with the parenting system
-----------------------------------------------

With compounds (aka unions), there is the problem that we have already implemented 
a sort of union with the genealogy concepts of children/parent, also 
more suttle since the union goes one way : moving A moves its children 
but not its parents.  This leads to some limitations in the compound class, to insure 
the compatibility with the genealogy system. When we move a compound,
an object may be unadequatly moved twice : once as an object of the
compound, once because it is a child and the parent has moved.

To avoid these problems, individual obects in a compound must
be isolated from the rest of the world : no parent, no child.
On the other hand, the compound itself, considered as a single
object can be nested in a genealogy tree as any regular object.
The limitations are only on its parts. 



The Compound class vs genealogy system
---------------------------------------

It is not clear a priori that we need a compound class to implement 
unions. If an  object O is a union of a,b,c,d , one could simply define 
an empty O and declare a,b,c,d as children of O. Then moving O would 
automatically the children and the camera rendering O would render 
a,b,c,d. The problems with this method is that intersection with O is not
possible, or more precisely requires too much work since 
the intersection does not intersect with the children.  
Moreover, all the markers that we have built in a,b,c,d 
are lost if we have access only to O. 

Compounds are useful:

* to mutualize the operations on the objects (intersection, colors...)
* to build libraries : the individual parts of the compound are
  accessible as compoundName.partName thus avoiding the collision of
  the names. Many parts may have the same name provided they are in
  different compounds 
* to help users define new object simply by patching parts without any
  knowledge on the technical details of primitive/elaborate objects. 
  
Genealogy (parent/child) system are useful:

* if we want to mutualize the movements, but however leaving the
  objects independant from each other
* because it is faster to describe : a one line declaration
  myObject.glued_on(anOtherObject) instead of the construction of a
  class. 




Implementation of CSG operations
---------------------------------

Each object may have an attribute  self.csgoperations
if it is affected by a csg operation.

The following integrity condition must be preserved:
self.csgOperations.csgKeyword="union"
if and only if self is a compound
(this hypothesis is used in the rendering :
recall that for a compound self, there are slaves, but no master
ie self is empty, thus we only render the slaves of self, not self
itself). 


self.csgOperations.keyword="union" | "intersection" | "difference"
self.csgOperations.slaves=[slave...]
slave= Primitive | Elaborate |  Compound

An other integrity condition is that if
self.csgOperations.csgKeyword="intersection"|"difference",
then each slave must be a child of self (this is used
implicitly when we move the shape to get consistant results).

The integrity conditions are automatically satisfied
if the csg operations are described using the
high-level functions amputed_by, intersected_by, and
the compound class. 

Implementation of compounds
----------------------------

Compounds objects are instances of the class Compound
defined in compound.py

As a compound can be defined as a single object in povray,
using the union keyword: implementation is easy, as 
long as the limitations explained above for the compatibility 
with the genealogy system are satisfied.

Move_alone move each slave of the compound but we never 
change the matrix  self.mapFromParts if self is a compound
(?? does not seem true when I read
the code, I think this self.mapFromParts is changed but unused). 
Using self.mapFromParts is tempting to factorize the movements,
but the primitive objects which are slaves of the compound
would not be updated in real time and it would be a mess. 








Architecture in Brief 
------------------------





* uservariables.py
* generic.py : define the class ObjectInWorld which basically defines 
  how objects are moved, parented, intersected,... 
* mathutils.py : define some math and the "pure math objects":
  plane,line,vectors..., defined above as primitive objects
* aliases.py : some global names useful to speed up the data capture.
* genericwithmaths: a continuation of generic, with some functions
  needing mathutils 
* elaborate.py : define the elaborate class and some instances 
* compound.py : define the compound class and some instances 
* povrayshoot.py : to produce a povray file from the python input.
* cameras.py
* lights.py : empty at the moment. 
* viewer.py : to see a povray file. 



Architecture in Detail (OUTDATED FROM HERE)
---------------------------------------------


mathutils.py
--------------

Contains the primitive objects:.... 
Also introduce the formalism of massic space. 

I shall use mass point formalism below. This is unusual, first let me explain
why and what it means. 

Recall that in math, adding 2 points in an affine space makes no sense, because
we find two different results if we make the computation twice with 
two different frames. To avoid these problems, mathematicias and physicists
have introduced the concepts of vectors and point with the rules 
point+vector=vector and point-point=vector which are valid operations.
From the informatics point of view, 
it is natural to use oriented object languages to declare two classes 
points and vector and so that the integrity of the comutations is automatically 
checked : the software raises an exception when the use tries the illegal operation 
of adding two points, even if these points are represented by a vector with 3 coordinates.

At the level of functions, maps on vectors are linear maps, and they
are represented by 3x3 matrices. Maps on points are affine maps. To allow 
matrix computations on the affine maps, the affine maps  are represented
with a matrix with bottom line = 0001 and affine points with coordinates
xyz are represented by the list xyz1. In theoretical terms, this comes
from the fact that an affine map is the restriction of linear map of the projective
Casting is necessary: when we add a point and a vector, we need 4 coordinates for the point.
and when we evaluate an affine map on a point : we need 4 coordinates for the point
if we want to use the matrix formalism.

Thus it is natural to make the distinction between points and vectors, 
both for integrity check and to allow easy matrix computations. 
Although this makes the code robust, this has drawbacks : vectors 
have 3 coordinates and points 4 coordinates and the code  
this makes the code longer since computing a-b needs to be implemented
several times : when both a,b are vectors,
when both a,b are points, or when a,b are point and vector.
An other drawbak, is that simple operations like taking the middle, 0.5p1+0.5p2
which make sense and are easy in coordinates, are not allowed any more 
and a special function Barycentre need to be implemented. This is bad 
in terms of readability since the code  Barycentre(p1,p2,.5,.5) is less
readable than 0.5*p1+0.5*p2

Summing up, using classes to distinguis points and vectors:
    the code is more  robust
    We have matrix formalism to evaluate maps both for points and vectors
But
    Points are implemented with three of four coordinates depending on the operation
    the code is longer with multiple implementations of addition and difference
    Simple operations like barycentre need special implementation.

Our goal is to imagine an implementation with the above advantages 
(integrity check and matrix formalism,), without the inconvenients.
We shall below introduce "mass points". This is a context which unifies 
points and vectors, thus we don't need multiple implementations of the same 
operations, and barycentric formalism is possible in this framework.
Finally, we always take 4 coordinates for both points and vectors. 

In practical terms, this means that an affine point in the affine space (x,y,z) 
has mass 1 and is represented by 4 coordinates (x,y,z,1)
A vector (x,y,z) has mass 0 and is represented by 4 coordinates (x,y,z,0)  
Both vectors and affine points are special cases of mass points (x,y,z,m).
The addition and external multiplication on mass points 
are the obvious ones. With this formalism, we recover the usual 
fact that point+vector=vector and point-point=vector. 
But we have new objects. For instance, 
And point of mass 1 + point of mass 1 = point of mass 2, an unusual object rarely used
in maths. The middle point 0.5p1+0.5p2 has mass 1, so it is a well defined point. 

 In this framework, we have:

* unification of affine points and vectors : both leave in the same space
  which makes addition and other operations easy to implement, while keeping
  a different type for theses objects. 
* possibility of simple notations for barycentre as a linear combination of affine points 
* easy formalism for computing with affine maps. In practical term, an affine map is written
  as a 4x4 matrix  with last line=0001 and this simple
  matrix formalism is good for composition, inversion and evaluation of maps.  
  The theoretical justification is that
  every affine map is the restriction of a unique linear map on the
  space of points of mass 1 and the affine maps identify with the massic maps which stabilize 
  the affine space. 


The only difficulty is that linear maps (ie maps on the vectors) do not naturally extend 
to the space of mass points. A  linear map f is represented by a 4x3 matrix with last
line equal 0.
Then  to homogeneize all the computations: we represent the map by 
a 4x4 matrix using an arbitrarily chosen last column. 
Thus all the maps are "massic maps" and the operations of composition 
and evaluation are unified for linear and affine maps in the space of massic maps. 

There are two simple choices for the last column C of a linear map. We may 
take C=0000 or C=0001. Both choice work well for composition and evaluation 
on vectors, but not for invertibility and linear combinations of maps.
With the second choice, an invertible linear map is represented
by a invertible matrix. With the first choice, the matrix of a linear map
f depend linearly on f. The choice C=0 is also useful to debug, as long as we don't use 
general massic maps but only affine and linear maps: the type of map, linear of 
affine, is checked by the bottom right coefficient of the matrix.
( not to be implemented: fragile since me may put general massic maps
in the game one day). 
We take the choice C=0, and we add  a function invert_as_linear_map in the 
class of massic functions to bypass the invertibility problem. 

As for the base changes, they are unified as follows. In the massic space, 
We have linear maps relative to a base. Giving two bases, we may compute a change of coordinates.
We identify a basis v1,v2,v3 of the vector space with the basis v1,v2,v3,v4 in the massic 
space, where v4=0001. Then the base change for the linear map is equal to the base 
change for the associated massic map. Similarly a frame in the afine space is a base in 
the massic space. Thus as long as the basis vector_base(v1,v2,v3) is equal 
to massic_base(v1,v2,v3,v4) and that frame(v1,v2,v3,v4)=massic_base(v1,v2,v3,v4), the
change of coordinates for the vector space and for the affine space are 
performed by the same operation: a base change in the massic space. 



elaborate.py
-------------

The class creation of an elaborate object is as follows. 
We define the class using a only list of parts and default values
in self.listOfParts.
Then, using a decorators, we define the init function, 
and for each part partName we add an attribute self.partName()
as documented before. Because the initial parts do not move, 
they have no genealogy connection with anything : self.parents and 
self.child are empty. The decorators also make the elements inherit 
from ObjectInWorld. 

# FOR PRIMITIVE
define the attributes and move_alone

# FOR ELABORATE
define self.parts, self.markers 
and finish the init by markers_as_functions(Self)


# FOR COMPOUND
define self.parts, self.markers 
and finish the init by self.build_from_parts(self) markers_as_functions(self) 

DONE
-----

- finir les squelettes et documenter/publier sur le newsgroups povray

- reflechir a enlever les guillemets pour selectionner une boite/un axe + doc  


   
TODO
---------

- verifier les objets construits depuis le changement d'intersection
 
- verifier que filmAllActors est debugge avec ce changement
 
- recycler les dessins de serrure qui sont dans solidOfRevolution.rst en exercice ?? 

- recycler le dessin de table dans footprint.rst qui est commente'

- voir pourquoi le Lathe ne marche pas quand la courbe est incluse
  dans y<0. 

  
copy et add_axis sont incompatibles



- finir et documenter skeleton :  permettre de  recuperer les angles
- permettre de poser un pied sur la pedale
  
  

- resoudre le allActors si possible en utilisant __main__
  more precisely, for each object constructed in mathutils.py or
  elaborate.py, get the grandparent frame, if this grand parent is
  main, add the object to the photoGroupList, 


  
- ajouter une page pour les conventions dans la doc
  - reflechir aux conventions ( radius ou diameter, interieur vers
  exterieur, nom avant l'objet dans les couples)

  - faire une fonction add_marker
  
  - delete pointInABox.png
  - documented point.glued_on act as a marker, and return point


- ajouter la fonction automove et flip pour positionner les cubes. 
- remplacer amputed_by with drilled_by

- comprendre comment gerer les emmerdes dues a numpy
  par exemple si a est un  ndarray, a in [2,5,7]
  renvoie un tableau au lieu d'un booleen

  
- construire les joints de 2 courbes et (apres verif qu'on l'a pas
  utilise') enlever coneOverPolygon et prismOverPolygon qui sont des
  cas particuliers de joints. 


- faire des prismes




- pour les creations d'objets: faire systematiquement des copies des
  objets passes en paraemetre en enlevant les enfants
- quand de nombreuses facon de creer : utiliser from_blabla en methode statique



- deployer en ecrivant la doc progressivement
- penser aux box des compounds
- idee directrice a verifier: les methodes sans argument qui renvoient
  des non mutables sont transformees en property.
- for each class document using general description,attributes,construction
- self.drill: couper avec un cylindre infini, 
- mettre un attribut draw_as pour les markers qui est une macro (bof)

