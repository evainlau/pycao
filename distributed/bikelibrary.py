"""
    This is Pycao, a modeler and raytracer interpreter for 3D drawings
    Copyright (C) 2015  Laurent Evain

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
import povrayshoot 
from cameras import *
from lights import *


class Bearing(Compound):
    def __init__(self,iDiameter=.02,mDiameter=.022,eDiameter=.030,thickness=.01,externalColor="Blue",internalColor="Silver"):
        out=Washer(origin,origin+thickness*Z,.5*eDiameter,.5*mDiameter).colored(externalColor)
        inner=Washer(origin,origin+thickness*Z,.5*mDiameter,.5*iDiameter).colored(internalColor)
        Compound.__init__(self,[["inner",inner],["outer",out]])
        self.box=out.box
        self.axis=out.axis

    def place_on_support(self,support):
        self.screw_on(support.axis(),adjustAlong=[self.point(.5,.5,0),support.support.point(.5,.5,1)])
        return self
        
class BearingSupport(Compound):
    def __init__(self,bearing,cylinder,clearance=.002,heightMargin=.002,metalThickness=.002,color="Bronze"):
        """
        This is a support for a bearing. This support is designed to be fixed on a cyllinder
        clearance: float. The space between the bearing and the walls
        heightMargin: float. How much the support is higher than the tube on which it is glued
        """
        height=2*cylinder.radius+heightMargin
        width=2*bearing.outer.radius+2*clearance
        bearingSupport=Cube(width,width+2*cylinder.radius,metalThickness)
        leftWall=Cube(height,width+cylinder.radius,metalThickness)
        #print(leftWall.segment(.5,None,.5,"ppp"),cylinder.radius)
        toCut=ICylinder(leftWall.segment(0.5,0,None,"ppp"),cylinder.radius)
        leftWall.amputed_by(toCut)
        leftWall.against(bearingSupport,X,X,Y,Y,adjustEdges=Y)
        rightWall=leftWall.copy().move(Map.linear(-X,Y,Z)).against(bearingSupport,X,-X,Y,Y,adjustEdges=Y)
        frontWall=Cube(width,height,metalThickness).against(bearingSupport,-Y,-Y,X,X)
        #workshopCut=Cube(height,height,metalThickness).colored("Black").against(leftWall,-Y,-Y,X,X)
        leftLine=bearingSupport.segment(0,None,1,"ppp")
        leftWall.rotate(leftLine,math.pi/2)
        rightLine=bearingSupport.segment(1,None,1,"ppp")
        rightWall.rotate(rightLine,-math.pi/2)
        frontLine=bearingSupport.segment(None,1,1,"ppp")
        frontWall.rotate(frontLine,math.pi/2)
        pointOnBearingAxis=frontWall.center-metalThickness*Y-.5*width*Y
        bearingAxis=Segment(pointOnBearingAxis,Z)
        bearing.screw_on(bearingAxis,adjustAlong=[bearing.point(.5,.5,0,"ppp"),bearingSupport.point(0,0,1,"ppp")])
        toCut=ICylinder(bearingAxis,bearing.inner.radius)
        bearingSupport.amputed_by(toCut)
        Compound.__init__(self,[["support",bearingSupport],["leftWall",leftWall],["rightWall",rightWall],["frontWall",frontWall]])
        self.colored(color)
        self.add_axis("steering",bearingAxis)

    def place_on_axis(self,segment,height,front=Y):
        #print(segment)
        #print("axis")
        #print(self.axis())
        pointOnAxis=Point.from_plane_and_line(plane(Z,point(0,0,height)),segment)
        self.screw_on(segment,adjustAlong=[self.support.center,pointOnAxis],adjustAround=[self.support.point(.5,1,0,"ppp"),segment.p1+front])
        #print("axis After")
        #print(self.axis())
        #self.screw_on(segment,adjustAlong=[self.support.center,pointOnAxis])
        #self.screw_on(segment)
        return self

            
class Crank(Compound):
    def __init__(self,length=.17, width=.03,depth=.01,pedalHoleDiameter=.02,squareSideLength=.01,color="Yellow"):
        cyl1=Cylinder(origin,origin+depth*Y,.5*width)
        cyl2=cyl1.copy().translate(length*X)
        myCube=Cube(length,depth,width)
        myCube.translate(cyl1.center-myCube.point(0,.5,.5, "ppp"))
        Compound.__init__(self,[cyl1,cyl2,["cube",myCube]])
        self.color=color
        self.add_axis("pedalAxis",cyl1.axis())
        self.add_axis("crankLongAxis",myCube.segment(None,.5,.5,"ppp"))
        self.add_axis("bottomBracketAxis",cyl2.axis())
        toCut=ICylinder(cyl1.axis(),pedalHoleDiameter/2)
        self.amputed_by(toCut)
        self.holeCenter=cyl1.center.copy().glued_on(self)
        
class Pedal(Compound):
    def __init__(self,width=.08,depth=.055,height=.01,axisDiameter=.02,offset=.03,pedalColor="Yellow",axisColor="Grey"):
        ped=Cube(width,depth,height).colored(pedalColor)
        ax=Cylinder(ped.point(1,.5,.5,"ppp"), ped.point(-offset,.5,.5,"npp"),axisDiameter/2).colored(axisColor)
        Compound.__init__(self,[["platform",ped],["screw",ax]])
        self.axis=ax.axis

class Crankset(Compound,ObjectInWorld):
    def __init__(self,interCranksDistance=.15,bbAxisRadius=.01,bbAxisColor="Red",plateColor="Red"):
           crank=Crank()
           ped=Pedal()
           crank.select_axis("pedalAxis")
           ped.screw_on(crank.axis(),adjustAlong=[ped.screw.center,crank.holeCenter])
           bbAxis=crank.select_axis("bottomBracketAxis")
           axisAlong=crank.select_axis("crankLongAxis")
           crank2=crank.copy().rotate(bbAxis,math.pi).rotate(axisAlong,math.pi).translate(+1*interCranksDistance*Y)
           ped2=ped.copy().rotate(bbAxis,math.pi).rotate(axisAlong,math.pi).translate(+1*interCranksDistance*Y)
           c=Cylinder(origin,origin+(interCranksDistance+.04)*Z,bbAxisRadius).colored(bbAxisColor)
           c.screw_on(bbAxis,adjustAlong=[c.center,.5*crank2.holeCenter+.5*crank.holeCenter,])
           plate=Sprocket(55).colored(plateColor)
           plate.screw_on(bbAxis,adjustAlong=[plate.point(0,.5,.5,"ppp"),crank2.cube.point(.5,1.2,.5,"ppp")])
           Compound.__init__(self,[crank,ped,crank2,ped2,["bracketAxis",c],plate])
           self.add_box("crankset",c.box())
           self.add_axis("axis",bbAxis)

           
class Sprocket(Cone):
    """
    A class for sprockets

    Constructor
    Sprocket(numberOfTeeth=14,sprocketThickness=.00185,toothTopLength=.0025,radiusPerTooth=0.002,color="Silver" ):
    numberOfTeeth=integer
    sprocketThickness=float
    toothTopLength=float=the length of  a tooth along the circumference
    radiusPerTooth=float such that the radius of the plate=radiusPerTooth*numberOfTeeth
    color: string
    """


    @staticmethod
    def __new__(cls,numberOfTeeth=14,sprocketThickness=.00185,toothTopLength=.0025,radiusPerTooth=0.002,color="Silver" ):
        radius=radiusPerTooth*numberOfTeeth
        c=Cone.__new__ (cls,origin,origin+sprocketThickness*Y,radius,radius+sprocketThickness)
        Cone.__init__(c,origin,origin+sprocketThickness*Y,radius,radius+sprocketThickness)
        return c
    
    def __init__(self,numberOfTeeth=14,sprocketThickness=.00185,toothTopLength=.0025,radiusPerTooth=0.002,color="Silver" ):
        self.color=color
        cutRadius=(2*3.1416*radiusPerTooth-toothTopLength)/2
        cylinder=Cylinder(self.point(.5,-0.0001,1,"ppp"),self.point(.5,1.1,1,"ppp"),cutRadius)
        angle=2*math.pi/numberOfTeeth
        for step in range(numberOfTeeth):
            self.amputed_by(cylinder)
            cylinder.rotate(self.axis(),angle)



class Cassette(Compound):
    """
    A class for Cassettes, ie union of sprockets

    Constructor
    Cassette(numberOfTeeth=[14,16,18],spaceBetweenSprockets=.005,sprocketThickness=.00185,)
    """
    
    def __init__(self,numberOfTeeth=[14,16,18],spaceBetweenSprockets=.005,sprocketThickness=.00185,
                 toothHeight=.006,toothTopLength=.0025,toothBottomLength=.012,radiusPerTooth=.002,color="Silver" ):

        slaves=[]
        i=0
        for nbTeeth in numberOfTeeth:
            sprocketObject=Sprocket(nbTeeth,sprocketThickness=sprocketThickness,
                                    toothTopLength=toothTopLength,
                                    radiusPerTooth=radiusPerTooth,color=color)
            if i==0: self.axis=sprocketObject.axis
            if i>0:  sprocketObject.against(slaves[-1][1],-Y,-Y,X,X,offset=(spaceBetweenSprockets-sprocketThickness)*Y)
            slaves.append(["sprocket"+str(i),sprocketObject])            
            i=i+1
        toCut=ICylinder(self.axis(),0.01)
        self.amputed_by(toCut)
        b=FrameBox([slaves[0][1].point(0,0,0),slaves[0][1].point(1,1,1),slaves[-1][1].point(0,0,0),slaves[-1][1].point(1,1,1)])
        self.add_box("box",b)
        Compound.__init__(self,slavesList=slaves)

class FrontWheel(Compound):
    """
    A class for Front wheels ie. with a rim, a hub, a tyre, and spokes, but no cassette 

    Constructor
    FrontWheel(tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.1,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=32,spokeRadius=0.0018,spokeColor='Black'
    ,rimOuterRadius=0.345,rimInnerRadius=0.320, axisRadius=.005)
    """
    def __init__(self,tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.1,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=26,spokeRadius=0.0018,spokeColor='Black'
                 ,rimOuterRadius=0.345,rimInnerRadius=0.320,axisRadius=.005):

        
        # tyre and rim
        tyre=Torus(tyreExteriorDiameter/2,tyreInternalRadius,Y,origin)
        rim=Washer(origin-0.015*Y,origin+0.015*Y,rimOuterRadius,rimInnerRadius)
        tyre.color=tyreColor
        rim.color=rimColor

        # the axis
        wheelPhysicalAxis=Cylinder(tyre.center-(hubWidth*.5+.02)*Y,tyre.center+(hubWidth*.5+.02)*Y,axisRadius).colored("Red")
        #hub
        hub=Cylinder(origin-hubWidth/2*Y,origin+hubWidth/2*Y,hubInternalRadius)
        hub.color=hubColor
        plaque1=Cylinder(origin,origin+0.0002*Y,hubExternalRadius)
        plaque1.color=hubColor
        plaque1.against(hub,Y,Y,X,X)
        plaque2=plaque1.copy()
        plaque2.against(hub,-Y,-Y,X,X)
        self.slaves=[["tyre",tyre],rim,plaque1,plaque2,["hub",hub],["axis",wheelPhysicalAxis]]

        # firstLeftSpoke
        spokeInit=plaque1.point(0.5,0.5,0.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),math.pi*4/numberOfSpokes)
        leftSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        leftSpoke.color=spokeColor

        # firstRightspoke
        spokeInit=plaque2.point(0.5,0.5,.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),-math.pi*4/numberOfSpokes)
        rightSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        rightSpoke.color=spokeColor

        # otherSpokes via rotation.
        for i in range(int(numberOfSpokes/2)):
            spoke1=leftSpoke.copy()
            self.slaves.append(spoke1.rotate(tyre.axis(),4*math.pi/numberOfSpokes*i))
            spoke2=rightSpoke.copy()
            self.slaves.append(spoke2.rotate(tyre.axis(),4*math.pi/numberOfSpokes*(i+0.5)))
        Compound.__init__(self,self.slaves)
        b=FrameBox([tyre.point(0,0,0),tyre.point(1,1,1),hub.point(0,0,0),hub.point(1,1,1)])
        self.add_box("wheel",b)
        self.add_axis("wheelAxis",hub.axis())

class RearWheel(Compound):
    """
    A class for Front wheels with a rim, a hub, a tyre, and spokes. 

    Constructor
    FrontWheel(tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.3,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=32,spokeRadius=0.0018,spokeColor='Black'
    ,rimOuterRadius=0.345,rimInnerRadius=0.320,axisRadius=.005)
    """
    def __init__(self,cassette=[12,14,16,20,22,25,30],tyreExteriorDiameter=0.70,tyreInternalRadius=0.02,wheelCenter=point(0,0,0)
    ,tyreColor='Green',rimColor='Red',hubColor='White',hubWidth=0.135,hubInternalRadius=0.025
    ,hubExternalRadius=0.05,numberOfSpokes=26,spokeRadius=0.0018,spokeColor='Black'
    ,rimOuterRadius=0.345,rimInnerRadius=0.320,axisRadius=.005):

        # tyre and rim
        tyre=Torus(tyreExteriorDiameter/2,tyreInternalRadius,Y,origin)
        rim=Washer(origin-0.015*Y,origin+0.015*Y,rimOuterRadius,rimInnerRadius)
        tyre.color=tyreColor
        rim.color=rimColor

        # the axis
        wheelPhysicalAxis=Cylinder(tyre.center-(hubWidth*.5+.02)*Y,tyre.center+(hubWidth*.5+.02)*Y,axisRadius).colored("Red")
        #hub
        myCassette=Cassette(cassette)
        hubWidth=hubWidth-myCassette.box().dimensions[1]
        hub=Cylinder(origin-hubWidth/2*Y,origin+hubWidth/2*Y,hubInternalRadius)
        hub.color=hubColor
        plaque1=Cylinder(origin,origin+0.0002*Y,hubExternalRadius)
        plaque1.color=hubColor
        plaque1.against(hub,Y,Y,X,X)
        plaque2=plaque1.copy()
        plaque2.against(hub,-Y,-Y,X,X)
        self.slaves=[["tyre",tyre],rim,plaque1,plaque2,["hub",hub],["axis",wheelPhysicalAxis]]
        myCassette.against(plaque1,-Y,-Y,X,X)
        self.slaves.append(["cassette",myCassette])

        # firstLeftSpoke
        spokeInit=plaque1.point(0.5,0.5,0.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),math.pi*4/numberOfSpokes)
        leftSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        leftSpoke.color=spokeColor

        # firstRightspoke
        spokeInit=plaque2.point(0.5,0.5,.01,"ppn")
        spokeEnd=tyre.point(0.5,0.5,0.02,"ppn")
        spokeEnd.rotate(tyre.axis(),-math.pi*4/numberOfSpokes)
        rightSpoke=Cylinder(spokeInit,spokeEnd,spokeRadius)
        rightSpoke.color=spokeColor

        # otherSpokes via rotation.
        for i in range(int(numberOfSpokes/2)):
            spoke1=leftSpoke.copy()
            self.slaves.append(spoke1.rotate(tyre.axis(),4*math.pi/numberOfSpokes*i))
            spoke2=rightSpoke.copy()
            self.slaves.append(spoke2.rotate(tyre.axis(),4*math.pi/numberOfSpokes*(i+0.5)))
        Compound.__init__(self,self.slaves)
        b=FrameBox([tyre.point(0,0,0),tyre.point(1,1,1),hub.point(0,0,0),hub.point(1,1,1),myCassette.point(0,0,0),myCassette.point(1,1,1)])
        self.add_box("wheel",b)
        self.add_axis("wheelAxis",hub.axis())


class Fork(Compound):
    def __init__(self,legLength=.3,upperTubeRadius=.02,lowerTubeRadius=.01,headLength=.1,headRadius=.02,entrax=.1):
        upperLeftLeg=origin+legLength*Z
        leftLeg=Cone(origin,upperLeftLeg,lowerTubeRadius,upperTubeRadius)
        rightLeg=leftLeg.copy().translate(entrax *X)
        upperRoundPart=Torus(entrax*.5,upperTubeRadius,Y,origin+legLength*Z+.5*entrax*X).amputed_by(plane(Z,upperLeftLeg))
        lowerHead=upperLeftLeg+.5*entrax*X+.5*entrax*Z
        slaves=[leftLeg,rightLeg,upperRoundPart]
        if headLength>0:
            head=Cylinder(lowerHead,lowerHead+headLength*Z,headRadius)
            slaves.append(head)
        Compound.__init__(self,slaves)
        self.add_axis("axis",Segment(origin+.5*entrax*X,Z))
        self.junction=lowerHead.glued_on(self)
