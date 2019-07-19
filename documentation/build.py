# pour creer la doc en local
# taper python buildDoc.py option
# avec option=small pour faire le make ou option=large pour tout recompiler les fichiers
import os
import sys
thisFileAbsName=os.path.abspath(__file__)
thisFileAbsDir=os.path.dirname(thisFileAbsName)
#print(thisFileAbsDir)
#print(thisFileAbsName)

#  construction of files to be executed 
path=thisFileAbsDir#+"/pycaogit/documentation/"
baseList1=os.listdir(thisFileAbsDir)
importList1=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildDoc.py' not in x and '__init__.py' not in x and 'conf.py' not in x, baseList1)
absList1=[path+"/"+File for File in importList1]


path=thisFileAbsDir+"/examples"
baseList2=os.listdir(path)
importList2=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildDoc.py' not in x and '__init__.py' not in x, baseList2)
absList2=[path+"/"+File for File in baseList2]

#for f in absList1: print(f)
#print()
#for f in absList2: print(f)
#commande="rm "+thisFileAbsDir+"/docPictures/*"
#print(commande)
#os.system(commande)


if len(sys.argv)==1 or sys.argv[1]=="help":
    print("python3 buildoc images : to generate the images\npython3 buildoc html or python3 buildoc html  to build the html file in the local html dir after the images have been generated\nTo build in an other place use \"sphinx-build -b html sourceDir OutputDir\" in an existing OutputDir")
elif "images" in sys.argv:
    commande="rm "+thisFileAbsDir+"/docPictures/*"
    print(commande)
    os.system(commande)
    for myfile in absList1:
        print(myfile)
        os.system("python3 "+myfile)
        #__import__(base) # does not work for some unknoww reason
    
    for myfile in absList2:
        print(myfile)
        os.system("python3 "+myfile)
        #__import__(myfile)
        
if "html" in sys.argv:
    if len(sys.argv)<3: dirBuild="html"
    elif sys.argv[2]=="local":
        dirBuild="html"
    commande="cd "+str(thisFileAbsDir)+"; sphinx-build -b html . html"
    print(commande)
    #os.system(commande)
"""
TODO
- essayer d'automatiser le stderr et le stdOutput de ce script et de baisser la verbosite' de povray pour que ce soit exploitable
- comprendre pourquoi le prism linear fonctionne mais pas le prism Bezier dans examples
- ecrire un script qui copie et update le template pour compilation plutot que le install.py qui est une copie non dynamique du  template
- verifier que tout est bon pour la compil des pythons a la fac comme ici
- mettre des options au sphinx-buiild : a pout tout recompiler, py pour recalculer les pythons. 
   sortie sur master si branch=master, sur latest=si branch non master
      * python3 buildDoc images -> effacer au prealable; tjs en local
      * python3 buildoc html inDevOrLocalOrNumVersion
- dire sur la doc qu'on peut compiler en local sa machine sur un repertoire au moment du changement de branche
- supprimer les vieux liens 
"""
