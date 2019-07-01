

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
   
.. image:: ./material1.png

.. code-block:: python 

    p=plane(Z,origin)
    pig1=Pigment("Coral") # a color known by povray
    pig2=Pigment.from_photo("chene.png",dimx=3.,dimy=10.,symmetric=True) # a pigment constructed by Pycao
    normal2=Normal("bumps .25 scale .061") # A normal which is a valid povray string
    normal1=Normal("bozo 1.5 scale .04") # A normal which is a valid povray string
    finish1=Finish(" ambient .35 diffuse .1 phong .023 phong_size 15")
    t1=Texture(pig1,normal1,finish1) # We put the elements in a texture
    t2=Texture(pig2,normal2,finish1)
    p.textured(t2) # we apply on our object
    s=Sphere(origin+.35*Z,.5).textured(t1).scale(1.05,1.03,1)



Changing the textures
------------------------

Once the material has been defined, it is possible to enhance it.
We can add a string or a previously defined material to an existing
material.  And we can add a material to a previously
defined texture. It is also possible to change the object directly. Here is an example
and the code to expand our scene. 

.. image:: ./material2.png

.. code-block:: python 


    finish2=Finish(" phong .023 phong_size 15")
    finish2.enhance(" ambient .2 diffuse .08 ") #PNF items enhanced by a string
    t=Sphere(origin+.35*Z-1*X,.5).colored("Yellow").scale(1.9,1.03,1)
    t.texture.enhance(normal1).enhance(finish2) #Texture enhanced by a PNFT item 
    normal2=Normal("bumps .55 scale .061") # A normal which is a valid povray string
    p.add_to_texture(normal2) # enhancing the object directly rather than the texture. 


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


.. image:: ./material3.png

.. code-block:: python

    p=plane(Z,origin)
    c=Cube(1,1,1)
    d=c.clone().translate(2*X)
    e=d.clone().translate(2*X) 
    f=d.clone().translate(4*X)
		
    pig1=Pigment.from_photo("chene.png",dimx=2.,dimy=10.,center=None,symmetric=False)
    p.textured(pig1)
    pig2=Pigment.from_photo("parquet1.png",dimx=2.,dimy=3.,center=None,symmetric=False)
    #pig3=Pigment.from_photo("parquet1.png",dimx=2.,dimy=3.,center=None,symmetric=False)
    for ob in [c,d,e,f]:
        ob.textured(pig2)
    unleash_texture([c,d]) # Now, c,d  have a texture different from e,f
    d.rotate(X,3.14/2) # The pigment move both in d and c, sharing the same structure, but not in e,f on the right


Some constructs
-------------------


.. image:: ./material4.png

.. code-block:: python

    p=plane(Z,origin)
    pig1=Pigment.from_photo("parquet1.png",dimx=2,dimy=2,symmetric=True) # a pigment constructed by Pycao
    pig2=Pigment.from_photo("chene.png",dimx=2.,dimy=2.,symmetric=True) # a pigment constructed by Pycao
    pig3=Pigment("Blue")
    pig4=Pigment("Red")
    pig=Pigment.from_square(pig1,pig2,pig3,pig4)
    p.textured(pig)

