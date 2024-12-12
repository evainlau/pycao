# first I compute all pycao files, as any python file but those in a bad list
pycaoFiles := $(wildcard *.py)
badFiles= conf.py
pycaoFiles := $(filter-out $(badFiles),$(pycaoFiles))
pycaoFilesSuffixless=$(basename $(pycaoFiles))
# The rest files are obtained by removing one letter to the pycao file names
restFiles :=$(wildcard *.rst)
restFilesSuffixless=$(basename $(restFiles))
# Les fichiers pov deja compiles
povFiles := $(wildcard *.pov)
povFilesSuffixless:=$(basename $(povFiles))

pngFromPov:=$(povFiles:.pov=.png)
pngFromFiles:= $(wildcard *.png)
pngFromAll:= $(pngFromFiles) $(pngFromPov)


# Here I build a rules of the form myFilename1.pov:myFilename1.py  or myFilename1.pov:myFilename.py depending on the existence on the second file 
$(foreach file,$(povFilesSuffixless), $(eval  $${file}.pov :  $$(shell  if test -e $${file}.py ; then echo $${file}.py; else echo `echo $${file} | sed 's/.$$$$//g'`.py ; fi); python3 $$^))


# Here I build a rule of the form myFilename.rst  : myFilename1.py myFilename.py  myFilename2.py  . The right list is built from the existence of the files.
# if the file.rst needs updating, then it is touched 
$(foreach file, $(pycaoFilesSuffixless),  $(eval $(shell if test -e ${file}.rst ; then echo ${file}.rst.liste+=${file}.py  ; else echo `echo ${file} | sed 's/.$$//g'`.rst.liste+=${file}.py ; fi; )))
$(foreach file,$(restFiles),  $(eval $(file): $$($(file).liste); touch $(file)  ) )


.PHONY : allpovfiles allrestfiles allpngs html sphinxbuild

allpovfiles : $(povFiles)
html : $(restFiles); sphinxbuild 
allpngs : $(pngFromAll)

%.png : %.pov
	povray $^  # maybe with better options 

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
sphinxbuild:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
