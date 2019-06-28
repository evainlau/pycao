Lights
======

In the absence of light, the scene looks very dark. 
To get a  realistic scene,  we usually need ambient shadowless ignts
and oter lights that yield shadow. Each light has a color, which
can be rgb values or a valid povray string. For a rgb color, we can
increase intensity by increasing the  rgb values. A named color
already encodes  the intensity. For instance, white and grey have
the same proportions of rgb,  but white has more intensity than grey.

The lights can be moved, and glued in the genealogy system. However,
they are just light sources, not physical objects, thus they cannot be
used in compounds or intersections.

When a ligth is added in the scene, it is automatically added to
the existing cameras in the scene ( this can be overwritten using the
option cameralist). Thus the usual strategy with a unique camera is
to declaire it at the beginning of the file and then add the lights.
But you are free to do the way you want adding the camera
at the end of the file and using myCamera.lights.append(myligth)
if you prefer. 


.. code-block:: python

    p=Plane(Z,origin).colored("Grey")
    c=Cube(1,1,1).colored("Bronze")
    l=Light().hooked_on(origin+4*X+5*Z+2.8*Y) # a light. spotlight by Default, emitting everywhere around
    l.colored("Red")
    l.rgbed(0,1,0)
    # Uncomment the following to remove shadow
    #l.shadowlessed()
    # A light which emits cone of lights with defined angles
    l.spotlighted(fullLigthAngle=30,noLightAngle=60,look_at=origin)
    # A light emitting cylinders of light
    l.cylindered(fullLigthRadius=10,noLightRadius=20,look_at=origin)
    # Back to point light
    l.pointlighted()
    # to decrease intensity with distance, ditance parameter is where half of the intensity is achieved. Then decreases fast with a high power
    l.fade(distance=5,power=4)

.. image:: ./lights.png
