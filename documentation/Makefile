# first I compute all pycao files, as any python file but those in a bad list
pycaoFiles := $(wildcard *.py)
badFiles= conf.py
pycaoFiles := $(filter-out $(badFiles),$(pycaoFiles))
pycaoFilesSuffixless=$(basename $(pycaoFiles))
# The rest files are obtained by removing one letter to the pycao file names
restFiles :=$(wildcard *.rst)
restFilesSuffixless=$(basename $(restFiles))
# Les fichiers pov deja compiles
povFiles := $(wildcard generatedImages/*.pov)
badFiles= generatedImages/bike.pov generatedImages/drawer.pov generatedImages/maisonLau.pov generatedImages/polyhedral.pov
povFiles := $(filter-out $(badFiles),$(povFiles))
povFilesSuffixless:=$(basename $(povFiles))
povFilesNodirSuffixless:=$(notdir $(basename $(povFiles)))

pngFromPov:=$(povFiles:.pov=.png)
pngFromFiles:= $(wildcard generatedImages/*.png)
pngFromAll:= $(pngFromFiles) $(pngFromPov)
badFiles= generatedImages/bike.png generatedImages/drawer.png generatedImages/maisonLau.png generatedImages/polyhedral.png
pngFromAll := $(filter-out $(badFiles),$(pngFromAll))


.PHONY : povs pngs html  pycao update help

help:
	@echo - make pycao pycaofile=file.py : lance python3 sur file.py
	@echo - make pngs : lance make sur tous les png trouvés
	@echo - make html: lance sphinx  _par defaut, le dir build est un lien dans public_html_ 
	@echo - make -B pngs : force le recalcul de tous les png, meme si plus recent que les perequisites
	@echo - make update = make pngs + make html
	@echo - make BUILDDIR=_tmp html: lance sphinx et builde dans un fichier temporaire pour verif 

# Here I build a rules of the form myFilename1.pov:myFilename1.py  or myFilename1.pov:myFilename.py depending on the existence on the second file 
$(foreach file,$(povFilesNodirSuffixless), $(eval  generatedImages/$${file}.pov :  $$(shell  if test -e $${file}.py ; then echo $${file}.py; else echo `echo $${file} | sed 's/.$$$$//g'`.py ; fi); echo le perequisite est $$^;  le target est $$@; python3 $$^ ))


# Here I build a rule of the form myFilename.rst  : myFilename1.py myFilename.py  myFilename2.py  . The right list is built from the existence of the files.
# if the file.rst needs updating, then it is touched 
$(foreach file, $(pycaoFilesSuffixless),  $(eval $(shell if test -e ${file}.rst ; then echo ${file}.rst.liste+=${file}.py  ; else echo `echo ${file} | sed 's/.$$//g'`.rst.liste+=${file}.py ; fi; )))
$(foreach file,$(restFiles),  $(eval $(file): $$($(file).liste); touch $(file)  ) )






povs : $(povFiles)
pngs : $(pngFromAll)


%.png : %.pov
	povray $^  2>>/dev/null 1>>/dev/null

%.py:
	echo warning $@ is missing

pycao :
	python3 $(pycaofile)

update: pngs html

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
html:$(restFiles)
	#@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"  $(SPHINXOPTS) $(O)	
	cd ../.. && CURDIR := $(shell pwd) && make html
