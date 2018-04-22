"""
    This is Pycao, a modeler and raytracer interpreter for 3D drawings
    Copyright (C) 2015  Laurent Evain

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

myPovFile="/tmp/pycaoOutput.pov" # the place to store the photo
defaultImageHeight=620 # in pixels
defaultImageWidth=600
filmAllActorsDefault=False # Not to change, since there are bugs at the moment in some objects which show up too many parts
includedFiles=["colors.inc","metals.inc","textures.inc","shapes.inc"]
defaultBackground="background {Blue}"
################################################################
#    Geometry
################################################################

screwPositiveRotations=True # ie rotation(axis,angle) "screws" when one looks  towards the axis and 
# the graphical representation in 3D has x on right, y in front and z up.  



################################################################
#    Lights and colors
################################################################
defaultLightType="spotlight"
# Ambient
defaultAmbientRgb=[.307,.307,.307]
defaultAmbientRgbIntensity=1.2
# lights with shadow
shadowlightDefaultRgb=[.522,.522,.522]
defaultShadowlightRgbIntensity=2# Same thing for lights with shadow
# lights without shadow
shadowlesslightDefaultRgb=[.322,.322,.322]
defaultShadowlesslightRgbIntensity=.3# Same thing for lights without shadow
# usual solid objects
defaultRgb=[.25,.25,0] 
defaultDiffuseMultiplier=.6
defaultAmbientMultiplier=.15
