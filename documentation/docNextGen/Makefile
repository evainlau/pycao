# first I compute all pycao files, as any python file but those in a bad list
pycaoFiles := $(wildcard *.py)
badFiles= conf.py
pycaoFiles := $(filter-out $(badFiles),$(pycaoFiles))
# The rest files are obtained by removing one letter to the pycao file names
restFiles := $(foreach pkfile,$(pycaoFiles), $(shell echo $(pkfile)| sed 's/..py/.rst/' ))
# Les fichiers pov deja compiles
pycaoFiles := $(wildcard *.pov)
# for each pycao files with name NAM construct a variable NAM_POVS with value the list
# of pov compatible

myrule= index.rst : index.py ;	echo NONE

#$(myrule)

%.rst :  %2.py %1.py 
	$(shell echo yhu)
	echo DONE

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
