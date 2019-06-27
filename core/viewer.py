from uservariables import *
from generic import *
from mathutils import *
from aliases import *
from genericwithmaths import *
from elaborate import *
from compound import *
import povrayshoot 
from cameras import *


from subprocess import call
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


from os.path import expanduser




class ViewerWindow(Gtk.Window):

    # les callback
    def show_camera_info(self):
        string="camera.hooked_on(point("+str(math.ceil(self.camera.location[0]*100)/100)+","+str(
            math.ceil(self.camera.location[1]*100)/100)+","+str(math.ceil(self.camera.location[2]*100)/100)+"))"
        string+="\n"
        string+="camera.lookAt=point("+str(math.ceil(self.camera.lookAt[0]*100)/100)+","+str(
            math.ceil(self.camera.lookAt[1]*100)/100)+","+str(math.ceil(self.camera.lookAt[2]*100)/100)+")"
        string+="\n"        
        string+="camera.angle="+str(math.ceil(self.camera.angle*100)/100)
        self.buttonInfo.set_label(string)
    def camera_string_to_file(self):
        string=povrayshoot.camera_string(self.camera)
        with open(self.camera.file, "a") as myfile:
            myfile.write(string)
        self.camera.pov_to_png()
        self.image.set_from_file(self.camera.imageFile)
        self.show_camera_info()
    def zoom_image(self,widget,zoomFactor):
        self.camera.zoom(zoomFactor)
        self.camera_string_to_file()
    def view_from(self,widget,vector):
        if vector != "":
            self.camera.location=self.camera.defaultDistance*vector+self.camera.lookAt
            self.camera_string_to_file()
    def move_point_looked_at(self,widget,vector):
        self.camera.lookAt+=vector
        self.camera_string_to_file()
    def move_forward(self,widget,value):
        self.camera.location+=value*(self.camera.lookAt-self.camera.location).normalized_clone()
        self.camera_string_to_file()
    def hlook_at(self,widget,value):
        self.camera.compute_frame_vectors()
        self.move_point_looked_at(widget,value*self.camera.rightVector)
    def vlook_at(self,widget,value):
        self.move_point_looked_at(widget,value*self.camera.sky)
    def rotate_view(self,widget,angle=.5,lateral=1,vertical=0):
        self.camera.compute_frame_vectors()
        myVector=vertical*self.camera.rightVector+lateral*self.camera.sky
        self.camera.location.rotate(line(self.camera.lookAt,myVector),-angle)
        self.camera_string_to_file()
    def hrotate(self,widget,value):
        self.rotate_view(widget,angle=value,lateral=1,vertical=0)
    def vrotate(self,widget,value):
        self.rotate_view(widget,angle=value,lateral=0,vertical=1)

        
    dico={"zoom":{-4:.2,-3:.5,-2:.8,-1:.95,1:1.05,2:1.2,3:2,4:4},"HorizontalRotate":{-4:-1.6,-3:-.4,-2:-.1,-1:-.025,1:.025,2:.1,3:.4,4:1.6},
          "VerticalRotate":{-4:-1.6,-3:-.4,-2:-.1,-1:-.025,1:.025,2:.1,3:.4,4:1.6},
          "MoveEyeHorizontally":{-4:-1.5,-3:-.25,-2:-.05,-1:-.01,1:.01,2:.05,3:.25,4:1.5}
          ,"MoveEyeVertically":{-4:-1.5,-3:-.25,-2:-.05,-1:-.01,1:.01,2:.05,3:.25,4:1.5}
          ,"MoveForward":{-4:-1.5,-3:-.25,-2:-.05,-1:-.01,1:.01,2:.05,3:.25,4:1.5}
          ,"ParallelViews":{-4:-X,-3:X,-2:-Y,-1:Y,1:-Z,2:Z,3:"",4:""}
    }

        
    def update_button(self,widget,toCall,value,label):
        try:
            widget.disconnect(widget.handler)
        except:
            pass
        value=ViewerWindow.dico[label][value]
        widget.handler=widget.connect("clicked",toCall,value)
        widget.set_label(str(value))
        
    def update_buttons(self,widget,toCall,label):
        widgetList=[[self.buttonIntensity1,-4],[self.buttonIntensity2,-3],[self.buttonIntensity3,-2],
                    [self.buttonIntensity4,-1],[self.buttonIntensity5,1],[self.buttonIntensity6,2],
                    [self.buttonIntensity7,3],[self.buttonIntensity8,4]]
        for w in widgetList:
            self.update_button(widget=w[0],toCall=toCall,value=w[1],label=label)

        
    def __init__(self,cameraSource=None):
        Gtk.Window.__init__(self, title="Povray Viewer")
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        # the camera and the image
        if cameraSource is None:
            camera=Camera()
            camera.quality=9
            Camera.showImage=False # When povray computes the image,does not pop-up
            camera.location=origin-3*Y+2*Z
            camera.imageHeight=defaultImageHeight # in pixels
            #camera.imageWidth=500
            #camera.zoom(1)
            tmpFile="/tmp/viewer"
            camera.file=tmpFile+".pov"
            camera.imageFile=tmpFile+".png"
            camera.lookAt=origin
        else:
            camera=cameraSource
            (root,ext)=os.path.splitext(camera.file)
            camera.imageFile=root+".png"            
        self.camera=camera
        self.camera.pov_to_png()
        self.image = Gtk.Image()
        self.image.set_from_file(camera.imageFile)


        # The button containing the image
        grid = Gtk.Grid()
        self.add(grid)        
        button1 = Gtk.Button()
        button1.add(self.image)
        grid.attach(button1,0,0,1,10)
        self.buttonInfo = Gtk.Label()
        self.buttonInfo.set_selectable(True)
        grid.attach(self.buttonInfo,1,9,3,1)
        
        
        # Radio buttons
        widgetList=[["buttonMenu1","zoom",self.zoom_image],["buttonMenu2","HorizontalRotate",self.hrotate],
                    ["buttonMenu3","VerticalRotate",self.vrotate],["buttonMenu4","MoveEyeHorizontally",self.hlook_at],
                    ["buttonMenu5","MoveEyeVertically",self.vlook_at],["buttonMenu6","MoveForward",self.move_forward],
                    ["buttonMenu7","ParallelViews",self.view_from]]
        i=0
        for w in widgetList:
            if i==0: reference=None 
            else: reference=getattr(self,widgetList[0][0])
            button=Gtk.RadioButton(group=reference,label=w[1])
            button.connect("toggled", self.update_buttons,w[2],w[1])
            grid.attach(button, 2, i, 1, 1)            
            button.show()
            setattr(self,w[0],button)
            i=i+1
        
        # Buttons which perform action 
        widgetList=[["buttonIntensity1",-4],["buttonIntensity2",-3],["buttonIntensity3",-2],["buttonIntensity4",-1],
                    ["buttonIntensity5",1],["buttonIntensity6",2],["buttonIntensity7",3],["buttonIntensity8",4]]
        for w in widgetList:
            button=Gtk.Button(label=w[1])
            setattr(self,w[0],button)
            grid.attach(button, 3, w[1]+4, 1, 1)            
        self.update_buttons(None,self.zoom_image,"zoom")

        grid.show()
        self.show_all()
        self.show_camera_info()
        Gtk.main()
