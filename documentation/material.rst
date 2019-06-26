==========
Material
=========

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

   
Simple  use of Colors and textures
---------------------------------------------------

.. code-block:: python 

   myObject.colored(myColor) # myColor is a String known to    povray. Look at Povray doc for the list of allowed strings
   myObject.rgbed(r,g,b)# rgb numbers in [0,1] for red,green,blue. 
   myObject.rgbed(r,g,b,t)# rgb as above, t   for transparency, t=0 is   opaque, t>0

   myObect.textured(myTexture) #myTexture=string in the list of  predifined povray Texture. Look at Povray doc for the list of allowed strings

More complex constructions
-----------------------------------------
