# pour creer la doc en local
# taper python3 buildDoc.py option
# avec option=small pour faire le make ou option=large pour tout recompiler les fichiers
import os
import sys
thisFileAbsName=os.path.abspath(__file__)
thisFileAbsDir=os.path.dirname(thisFileAbsName)
#print(thisFileAbsDir)
#print(thisFileAbsName)

# First, we clean the repository of images
commande="rm "+thisFileAbsDir+"/generatedImages/*"
#print(commande)
os.system(commande)



# we copy the template to check it in the doc build
pyTemplate=thisFileAbsDir+"/../core/template.py "
pyTemplateModif=thisFileAbsDir+"/../core/templateModif.py "
povTemplate=thisFileAbsDir+"/../core/templateModif.pov"
pngTemplate=thisFileAbsDir+"/../core/templateModif.png "
pngTemplateTogo=thisFileAbsDir+"/generatedImages/install1.png "
os.system("sed -e 's/camera.show/camera.pov_to_png/g' "+pyTemplate+" >"+pyTemplateModif)
os.system("python3 "+pyTemplateModif)
os.system("rm "+pyTemplateModif+povTemplate)
os.system("mv "+pngTemplate+pngTemplateTogo)

#  construction of files to be executed 
path=thisFileAbsDir#+"/pycaogit/documentation/"
baseList1=os.listdir(thisFileAbsDir)
importList1=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildImages.py' not in x and '__init__.py' not in x and 'conf.py' not in x, baseList1)
absList1=[path+"/"+File for File in importList1]


path=thisFileAbsDir+"/examples"
baseList2=os.listdir(path)
importList2=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildImages.py' not in x and '__init__.py' not in x, baseList2)
absList2=[path+"/"+File for File in baseList2]


#for f in absList1: print(f)
#print()
#for f in absList2: print(f)
#commande="rm "+thisFileAbsDir+"/generatedImages/*"
#print(commande)
#os.system(commande)



for myfile in absList1:
    print(myfile)
    os.system("python3 "+myfile)
    #__import__(base) # does not work for some unknoww reason

for myfile in absList2:
    print(myfile)
    os.system("python3 "+myfile)
    #__import__(myfile)

