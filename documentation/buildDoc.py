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
    print("parametre requis pour le scrpt. valeurs possibles: small or large")
elif sys.argv[1]=="large":    
    for myfile in absList1:
        os.system("python3 "+myfile)
        #__import__(base) # does not work for some unknoww reason
    
    for myfile in absList2:
        os.system("python3 "+myfile)
        #__import__(myfile)
        
if len(sys.argv)>1:
    commande="cd /users/evain/subversion/sitesWeb/pro/; make html"
    print(commande)
    os.system(commande)
