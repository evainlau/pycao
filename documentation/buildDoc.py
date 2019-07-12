# pour creer la doc en local
# taper python buildDoc.py option
# avec option=small pour faire le make ou option=large pour tout recompiler les fichiers
import os
import sys
fileName=os.path.abspath(__file__)
dirName=os.path.dirname(fileName)
#print(dirName)
#print(fileName)

#  construction of files frome diistributed
path=dirName#+"/pycaogit/documentation/"
initialList1=os.listdir(path)
path+="/examples"
initialList2=os.listdir(path)

#coreList=filter(lambda x:'.py' in x and ".pyc" not in x, initialList1)
importList1=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildDoc.py' not in x and '__init__.py' not in x, initialList1)
importList2=filter(lambda x:'.pyc' not in x and '.py' in x and 'buildDoc.py' not in x and '__init__.py' not in x, initialList2)

restList=filter(lambda x:'.rst' in x, initialList1)

#print(list(restList))
#from itertools import filterfalse
#coreList=filterfalse(lambda x:True, initialList1)
#print(coreList)

#for f in importList1: print(f)
#a=1/0
#importList1=["curvesPrism.py"]
if len(sys.argv)==1:
    print("parametre requis pour le scrpt. valeurs possibles: small or large")
elif sys.argv[1]=="large":    
    for myfile in importList1:
        directory=os.path.dirname(os.path.realpath(myfile))
        base=os.path.basename(myfile)
        myfile=directory+"/"+base
        print(myfile)
        os.system("python "+myfile)
        #__import__(base) # does not work for some unknoww reason

    
    for myfile in importList2:
        directory=os.path.dirname(os.path.realpath(myfile))
        base=os.path.basename(myfile)
        myfile=directory+"/examples/"+base#os.path.splitext(base)[0]
        os.system("python "+myfile)
        #__import__(myfile)
        
if len(sys.argv)>1:
    commande="cd /users/evain/subversion/sitesWeb/pro/; make html"
    print(commande)
    os.system(commande)
