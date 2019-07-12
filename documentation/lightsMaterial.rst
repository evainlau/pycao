**************************
Lights and material
**************************

Lights and material are poorly implemented. Basically, we need to
enter the povray string. 

Lights
-------
By default, in the template, the lights of the camera are defined by: 

.. code-block:: python

    camera.location=origin-5*X+0*Y+2*Z
    camera.povraylights="light_source {<"+ str(light.location[0])+","+str(light.location[1])+","+str(light.location[2])+ "> color White " + "}\n\n"

You may Change camera.povraylights with any string which is a valid
light string in povray. 


Texture
---------

We can easily define colors with

.. code-block:: python

    object.color='Red' # Red is a color known to povray
    object.color= '<0.5,0.5,0.5>' # rgb description
    object.color='<1.5,0.5,0.5,1,0>' # for transparence, see povray doc

If we want something more suttle, we directly introduce the povray
string we want, in which case the object.color is ignored: 

 
.. code-block:: python
		
    self.material="YourPovrayString"

For instance: 

.. code-block:: python

    cyl2.material="pigment { brick  brick_size 2 mortar 0.2 }"

is a valid string.

Other Povray string
-------------------
If some attributes are still missing, recall that we can enter any 
povray string in camera.preamble which is put at the beginning of the
povray file. Default to '#include "colors.inc" \n#include "metals.inc" \nbackground {Blue}\n\n'
