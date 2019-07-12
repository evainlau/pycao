Bugs
=========

The option camera.filmAllActors works well only
in simple situation. It is very buggy. In principle, it is supposed
to collect the objects constructed by the user, but there are often
plenty of objects constructed in intermediate computations performed
by the Pycao engine that appear.
At the moment, I have no idea how to bypass this problem
in a simple way.

If some unwanted objects appear on the render, just
set camera.filmAllActors=False and define
camera.actors=[theListOfParentsThatGenerateTheWholeScene]


