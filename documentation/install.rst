***************************************
Installation 
***************************************

In this page, we shall see how to set up pycao and run 
our first file. 

Perequisites and Download
--------------------------

* pycao requires povray,python, scipy, numpy and pygobject
  (gi). Please install them on your system. Pygobject is not absolutly
  necessary (see below ). 
  
I suppose that you installed Pycao in "/home/myName"   Please adapt the
following to  your directory name. 

* Download pycao on github https://github.com/evainlau/pycao
  and drop it off in /home/myName/. 



Check the installation 
------------------------------------------------

* Open the file /home/myName/pycao/core/template.py. In the first lines,
  there is a variable "pycaodir". Change the
  the value of that variable pycaoDir so that it corresponds to your case.
  You probably want something like
  "pycadir=/home/myName/pycao/core/"
* In case, you have have not installed pygobject, comment the line
  "camera.show" at the end of the file and uncomment the next line "camera.show_without_viewer"
  Everything will work, but you will lose the possibility to change
  the zoom and the camera position interactivly with a graphical interface. 
* At the end of the file, optionnally change the value of camera.file
  which is the place where the povray file is created.
* Save the file and exit. 
* in a terminal,  run the command "python /home/myName/core/template.py"
  and you should see the first 3D picture you have created with pycao

.. image:: ./docPictures/install1.png


Preparing your future projects
--------------------------------
	   
In the pycao directory, there are two template files: template.py, and
emptyTemplate.py. They are designed to be inserted in the file you
work. A good idea is to put the templates in read-only mode
after you have set the initialisation of the variable pycaoDir
to avoid unwanted overwrite.
However, if you make a mistake and overwrite these files, you always have the possibility to
pull these files again from github without reinstalling.

The file template.py contains a few simple objects. It
is good for beginners who can play with the 3D objects in the file
to make tests. In contrast, emptyTemplate.py is useful when we are
comfortable with Pycao and want an empty file to work immediatly
without deleting unnecessary objects. 



Practice
--------------------------------------------------

* copy the file /home/myName/pycao/core/template.py to /home/myName/theFileNameOfYourChoice.py 
* open theFileNameOfYourChoice.py with an editor
* increase the value of the camera.zoom
* run the command "python theFileNameOfYourChoice.py" again
  and you should see the same 3D picture as above, but larger
* The file we played with contains several comments. Read them and 
  try to modify some values to see how this impacts the 3D picture.




