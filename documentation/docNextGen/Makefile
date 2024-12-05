# first I compute all pycao files, as any python file but those in a bad list
pycaoFiles := $(wildcard *.py)
badFiles= conf.py
pycaoFiles := $(filter-out $(badFiles),$(pycaoFiles))
# The rest files are obtained by removing one letter to the pycao file names
restFiles := $(foreach pkfile,$(pycaoFiles), $(shell echo $(pkfile)| sed 's/..py/.rst/' ))
# Les fichiers pov deja compiles
povFiles := $(wildcard *.pov)
povFilesSuffixless=$(basename $(povFiles))



$(info    listePov is $(povFiles))
$(info    listePovSuffixless is $(povFilesSuffixless))






# Here I build a rules of the form myFilename1.pov myFilename1.py  or myFilename1.pov myFilename.py depending on the existence on the second file 

$(foreach file,$(povFilesSuffixless), $(eval  $${file}.pov :  $$(shell  if test -e $${file}.py ; then echo $${file}.py; else echo `echo $${file} | sed 's/.$$$$//g'`.py ; fi); python $$^))
#$(foreach file,$(povFilesSuffixless), $(eval  $$(info $${file}.pov :  $$(shell  if test -e $${file}.py ; then echo $${file}.py; else echo `echo $${file} | sed 's/.$$$$//g'`.py ; fi))

.PHONY : allpovfiles
allpovfiles : $(povFiles)

# this rule is to build a particular python file
*.py:
	python  $@.py



here.py:
	touch here



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
