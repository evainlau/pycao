

Material
=========


Simple  use of Colors and textures
---------------------------------------------------

The basic appearance of an object is controlled by a color defined as
a name or with 3 numbers in a rgb format. We have used this many times
in the examples so far. It is also very simple to
import a texture which is predeclared in Povray. 


.. code-block:: python 

   myObject.colored(myColor) # myColor is a String known to    povray. Look at Povray doc for the list of allowed strings
   myObject.rgbed(r,g,b)# rgb numbers in [0,1] for red,green,blue. 
   myObject.rgbed(r,g,b,t)# rgb as above, t   for transparency, t=0 is   opaque, t>0

   myObect.textured(myTexture) #myTexture=string in the list of  predifined povray Texture. Look at Povray doc for the list of allowed strings

   
Defining our textures
-----------------------------------------

The material is what is applied to an object to look nice. It may be a
color or a wood aspect, a mirror finish or some granularity to mimic
a non smooth object.

Now we approach the question of defining our own material
to get nice looking objects. In contrast to the previous modules, the module
controlling the material is tied to povray.
   
There are three types of material:

- Pigments : governing the color of an object. May be imported from a
  photo projected on the object. May include transparency

- Normals : governs if the object is smooth and polished, or bumpy
  with rugosity. It determines the angles of the reflected  light,
  when the light hits the object. It mimics the rugosity that we feel
  when we pass our finger on the object. 

- Finishes : governs the quality of the light after rebounding on the
  object. On a mirror, a large amount of light is
  transmitted and the light is not colored when it hits  the mirror.
  The light that reflects on your blue jeans varies with the incident
  light, but, in contrast to a mirror, the refected light is always
  rather blue. In other words, the finish contains the information
  to compute the reflected light when you know the incident light
  and the pigment of the object,. It encodes the interaction between
  the incident light and the Pigment of the object.

- A texture is a container in which we add Pigments, normal, and
  textures. 

The simplest way to control the aspect of an object is to define a
pignment, normal and finish, a texture from them, and to apply on
our object. 
   
.. image:: ./docPictures/material11.png


.. literalinclude:: material1.py
   :start-after: bbloc1
   :end-before: ebloc1




Changing the textures
------------------------

Once the material has been defined, it is possible to enhance it.
We can add a string or a previously defined material to an existing
material.  And we can add a material to a previously
defined texture. It is also possible to change the object directly. Here is an example
and the code to expand our scene. 

.. image:: ./docPictures/material12.png

.. literalinclude:: material1.py
   :start-after: bbloc2
   :end-before: ebloc2


Moving, gluing, relaxing
--------------------------

The textures can be moved, resized like any other object. They
automatically move with the object that support the texture. 
This is used for instance to have photo-realistic wood textures. The grain of
the wood must have the correct orientation thus the wood texture needs to
follow the object in its movements. In particular,
the movement of the object may impact the appearance of an
other object if they share the same
texture. It is possible to unleash textures to avoid this phenomena
when necessary.  


On the image, we see how to create a texture
from a photo in the x,y plane. Some cubes share the same texture and some don't.


.. image:: ./docPictures/material2.png

.. literalinclude:: material2.py
   :start-after: bbloc1
   :end-before: ebloc1

	   

Some constructs
-------------------


.. image:: ./docPictures/material3.png

.. literalinclude:: material3.py
   :start-after: bbloc1
   :end-before: ebloc1

