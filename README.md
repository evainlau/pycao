================================
 PYCAO
===============================

This is the pycao modeller.
In short, this is a tool to
describe a 3D-scene using
the python language, with plenty
of simplifying paradigms
( carrying objects in boxes,
genealogy system, compact mathematical notations,
markers ... ).
Then you can see your 3d objects
using povray as a plugin. 


The documentation  is available
on my home page
at the university of Angers.
http://math.univ-angers.fr/~evain/software/pycao/documentation/index.html


New in version 0.9:

- based on Python3+
- Tutorial close to final form
- Markers enhanced with easier notations
- Fully parametric coordinate free language for nearly all geometric operations
- Enhanced interpolation curves with speed control at the control points
- Amelioration of the Curve class for efficiency
- Material module consistent with the Pycao approach with simplifying paradigms ( was a dirty hack to Povray precedently)
  

Roadmap to Version 1.0:

- Needs a reference manual
- Document the possible geometric constructions possible, and the full list of objects possible
- The init functions should make possible to create the objects in whatever position with adequate positions
- Needs notations fully compatible with python peep recommandations (camelCase conventions and so on)
- Consistency of the notations: avoid the shortcuts without parenthesis for parameterless functions to improve readability

Roadmap to verson 1+, ideas for the future:

- efficiency: replace primitive and elaborate modules by a just-in time module which computes only the objects required on demand
- language add-ons necessary to handle films and animations
- language add-ons to facilitate photo-realistic renderings.
