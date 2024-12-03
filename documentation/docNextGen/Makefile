# first I compute all pycao files, as any python file but those in a bad list
pycaoFiles := $(wildcard *.py)
badFiles= conf.py
pycaoFiles := $(filter-out $(badFiles),$(pycaoFiles))
# The rest files are obtained by removing one letter to the pycao file names
restFiles := $(foreach pkfile,$(pycaoFiles), $(shell echo $(pkfile)| sed 's/..py/.rst/' ))
# Les fichiers pov deja compiles
povFiles := $(wildcard *.pov)
povFilesSuffixless=$(basename $(povFiles))
$(info    listePov is $(povFilesSuffixless))

none=$(foreach povfile,$(povFiles), $(povfile)_pyfile=$(shell echo $(povfile)| sed 's/..pov/.py/' ))

$(info $(essai.pov_pyfile))

# for each pycao files with name NAM construct a variable NAM_POVS with value the list
# of pov compatible

myrule= index.rst : index.py ;	echo NONE

dessin.py_pov := dessin1.pov dessin2.pov
schema1_pov := schema11.pov schema12.pov schema13.pov
schema_rest := schema1.py schema2.py 
listePycao= dessin.py schema1.py
listePycaoShort= dessin schema1
listeRest=schema
povFiles= essai1.pov essai2.pov essai.pov

$(info    listePycao is $(listePycao))

essai.pov_pyfile=here.py


$(povFiles) : $($@_pyfile)
	echo $^
	echo success
	echo $($@_pyfile)

here.py:
	touch here

$$($$@_pov):$(listePycao)
	echo $* est le target 
	echo le mb de droite est $^
	touch $^


.SECONDEXPANSION:
$(listeRest): $$($$@_rest)
	echo secondExpansion



#%.pov :
#	touch $@
#	echo povConstruit using 

%.rst:
	echo $@


%.png:%.pov
	echo povrayCall to build the png $@ for the corresponding pov file

#$(myrule)


%.py :
	echo in the py file $@, nothing to do


this: 
	#echo $(pycaoFiles)
	#echo $(restFiles)

buildThisFileForce: $@
	si c'est un fichier python, le pythonner
	si c'est un fichier rst, le sphinx-builder
	si c'est un fichier povray, le povray'

pythonThisFileMaybe:$@
	construireLalisteDesPovCorrespondantes

# Minimal makefile for Sphinx documentation
#


# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
#help:
#	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
