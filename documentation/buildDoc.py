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
importList1=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildDoc.py' not in x and '__init__.py' not in x, baseList1)
absList1=[path+"/"+File for File in importList1]
          
path=thisFileAbsDir+"/examples"
baseList2=os.listdir(path)
importList2=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildDoc.py' not in x and '__init__.py' not in x, baseList2)
absList2=[path+"/"+File for File in baseList2]

#for f in absList1: print(f)
#print()
#for f in absList2: print(f)

if len(sys.argv)==1:
    print("parametre requis pour le scrpt. valeurs possibles: html,python")
elif "python" in sys.argv:    
    for myfile in absList1:
        os.system("python3 "+myfile)
        #__import__(base) # does not work for some unknoww reason
    
    for myfile in absList2:
        os.system("python3 "+myfile)
        #__import__(myfile)
        
if "html" in sys.argv:
    commande="cd "+str(thisFileAbsDir)+"; sphinx-build -b html . html"
    print(commande)
    os.system(commande)
"""
TODO
- renommer les fichiers 
- enlever tous les code-blocks et les remplacer par des include litteral, avec begin-after et end-before
- retravailler someObjects.py pour pouvoir mettre allActors=True
- verifier que tout est bon pour la compil des pythons a la fac comme ici
- ajouter des fichiers pour le meuble et maison et ainsi supprimer les binaires inutiles
- mettre des options au sphinx-buiild : a pout tout recompiler, py pour recalculer les pythons. 
   sortie sur master si branch=master, sur latest=si branch non master
- dire sur la doc qu'on peut compiler en local sa machine sur un repertoire au moment du changement de branche
- supprimer les vieux liens 
"""
