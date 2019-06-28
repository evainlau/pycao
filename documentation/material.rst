

Material
=========


Simple  use of Colors and textures
---------------------------------------------------

The basic appearance of an object is controlled by a color defined as
a name or with 3 numbers in a rgb format. It is also very simple to
import a texture which is predaclared in Povray. 


.. code-block:: python 

   myObject.colored(myColor) # myColor is a String known to    povray. Look at Povray doc for the list of allowed strings
   myObject.rgbed(r,g,b)# rgb numbers in [0,1] for red,green,blue. 
   myObject.rgbed(r,g,b,t)# rgb as above, t   for transparency, t=0 is   opaque, t>0

   myObect.textured(myTexture) #myTexture=string in the list of  predifined povray Texture. Look at Povray doc for the list of allowed strings

   
More complex constructions
-----------------------------------------

In contrast to the geometry, the module controlling the material on
our objects is tied to povray. If we want to go beyond these simple
appearances, for instance to make a photo realistic object,
some explanations on the povray approach are
required. We explain only the basics, referring to the povray
documentation for more details. 
   
The material is what is applied to an object to look nice. It may be a
color or a wood aspect, a mirror finish or some granularity to mimic
a non smooth object. There are three types of material:

- Pigments : governing the color of an object. May be imported from a
  photo projected on the object. May include transparency

- Normals : governs if the object is smooth and polished, or bumpy
  with rugosity. It determines the angles of the reflected  light,
  when the light hits the object. It mimics the rugosity that you feel
  when you pass your finger on the object. 

- Finishes : governs the quality of the light after rebounding on the
  objecct. For instance, on a mirror, a large amount of light is
  transmitted and the light is not colored when it hits  the mirror.
  The light that reflects on your blue jeans varies with the incident
  light, but, in contrast to a mirror, the refected light is always
  rather blue. In other words, the finish contains the information
  to compute the reflected light when you know the incident light
  and the pigment of the object,. It encodes the interaction between
  the incident light and the Pigment of the object.

 - A texture is a container in which we add Pigments, normal, and
   textures. 

The textures can be moved, resized and glued like any other object. This is
used for instance to have photo-realistic wood textures. The grain of
the wood must have the correct orientation thus the wood texture needs to
follow the object in its movements.


.. image:: ./material1.png

On the image, we see the first example on how to create a texture
from a photo in the x,y plane. In the example,
some cubes share the same texture and some don't.
The example illustrates that the texture moves with the object
so that the movement of an object may impact the appearance of an
other object if two objects share the same
texture. 

.. code-block:: python

    p=plane(Z,origin)
    c=Cube(1,1,1)
    d=c.clone().translate(2*X)

    pig1=Pigment.from_photo("chene.png",dimx=2.,dimy=10.,center=None,symmetric=False)
    pig2=Pigment.from_photo("parquet1.png",dimx=2.,dimy=3.,center=None,symmetric=False)
    pig3=Pigment.from_photo("parquet1.png",dimx=2.,dimy=3.,center=None,symmetric=False)
    c.new_texture(pig2)#.colored("Green")
    d.new_texture(pig3)
    p.new_texture(pig1)
    # e and d share the same texture pig2, f does not since the clone has taken a copy of the texture
    e=d.clone().translate(2*X) 
    e.new_texture(pig3)
    f=d.clone().translate(4*X)
    d.rotate(X,3.14/2) # The pigment move both in d and e
