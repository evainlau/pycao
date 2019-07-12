

Construction of simple objects 
=================================

Examples
--------
The following objects are native in Pycao, ie. they
can be defined with one or two lines of code. 
We shall see in the next chapters how to intersect, move,
link them... to get the desired  3D-scene starting from these
objects.

Te code below indicates how to use these objects. For objects built on
curves, the full syntax will be explained in the chapter on curves but
we include them here so that you are informed of the possibilities. 

.. image:: ./docPictures/someObjects.png


.. code-block:: python


   grayGround=plane(Z,origin).colored('Gray' ) # a plane with normal the vector Z=vector(0,0,1) containing the origin
   # The possible colors are the colors described in colors.inc in povray. 

   brownCube=Cube(1,2,2).colored("Brown") # The two opposite corners of the cube are origin and point(1,2,2)
   brownCube.translate(-2*X-Y) 
   
   closedPinkCylinder=Cylinder(start=origin+2*Y,end=origin+2*Y+.4*Z,radius=0.5).colored('SpicyPink')

   axis=line(point(0,-4,0),point(0,-4,1))
   infiniteYellowCylinder=ICylinder(axis,0.5).colored('Yellow') #an infinite cylinder of radius 0.5

   redSphere=Sphere(origin+.8*Z,.8).colored('Red') #arguments=center and radius

   silverWasher=Washer(point(3,3,0),point(3,3,0.3),.3,0.15).colored('Silver') #arguments; start,end,externalRadius,internalRadius
   
   blueOpenCylinder=Cylinder(start=origin+2*Y,end=origin+2*Y+0.3*Z,radius=0.5,booleanOpen=True) # a vertical Cylinder
   blueOpenCylinder.colored('Blue')
   blueOpenCylinder.translate(-4*X)

   yellowTorus=Torus(0.5,0.1,Z,origin)
   yellowTorus.named("Torus")
   p1=point(-2,0,0)
   p2=point(0,3,0)
   # The torus is sliced using two planes containing the axis and one point pi. 
   yellowTorus.sliced_by(p1,p2,acute=False).colored("Yellow").translate(-2*X+3.5*Y+0.5*Z)
   
   r=0.2
   curve=Polyline([origin,2*Y+X,Y+X,Y+2*X,-3*Y+X])# a polyline with control points prescribed. See the curve chapter for more details.
   cyanLathe=Lathe(curve).colored("Cyan").move(Map.affine(r*X,r*Z,r*Y,origin+2*X+1.4*Y))

   r=0.2
   curve=BezierCurve([origin,2*X+Y,X+Y,X+2*Y]) # A Bezier curve with control points prescribed. See the curve chapter for more details.
   orangeLathe=Lathe(curve).colored("Orange").move(Map.affine(r*X,r*Z,r*Y,origin+4*X))
   
   r=0.15
   curve=PiecewiseCurve.from_interpolation([origin+Y+2*X,3*Y+X,2*Y+X,Y+X,X],closeCurve=True)
   bronzeLathe=Lathe.fromPiecewiseCurve(curve).colored("Bronze").move(Map.affine(r*X,r*Z,r*Y,origin-4*X+.5*Z))
   
   p0=origin;
   p1=p0-X+Y;p2=p1+X+Y;p3=p2+X-Y;
   i=1.4
   # Below an interpolation curve through the control points
   curve4=PiecewiseCurve.from_interpolation([origin,p1,p2,p3,origin],closeCurve=True)
   curve7=PiecewiseCurve.from_interpolation([p2,p3,origin,p1,p2],closeCurve=True).scale(i,i,i).translate(1.7*Z)
   # The union of segments [curve7(t),curve4(t)]:
   HunterGreenRuledSurface=RuledSurface(curve7,curve4).colored("HuntersGreen").translate(-3.2*Y+3*X)

   violetCone=Cone(origin,origin+2*Z,.6,2 ).colored("Violet").translate(-4.5*X-4*Y)# arguments: start,end,radius1,radius2
