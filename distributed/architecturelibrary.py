
class DoorHandle(Compound):
    def __init__(self,depth=.08,length=.10,eDiameter=.030,color="Silver"):
        tube1=Cylinder
        out=Washer(origin,origin+thickness*Z,.5*eDiameter,.5*mDiameter).colored(externalColor)
        inner=Washer(origin,origin+thickness*Z,.5*mDiameter,.5*iDiameter).colored(internalColor)
        Compound.__init__(self,[["inner",inner],["outer",out]])
        self.box=out.box
        self.axis=out.axis

    def place_on_support(self,support):
        self.screw_on(support.axis(),adjustAlong=[self.point(.5,.5,0),support.support.point(.5,.5,1)])
        return self
