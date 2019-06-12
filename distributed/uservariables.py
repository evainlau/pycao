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

myPovFile="pycaoOutput.pov" # the place to store the photo
defaultImageHeight=620 # in pixels
defaultImageWidth=900
filmAllActorsDefault=False # Not to change, since there are bugs at the moment in some objects which show up too many parts
includedFiles=["colors.inc","metals.inc","textures.inc","shapes.inc","stones1.inc","woods.inc"]
defaultBackground="background {Blue}\n"
################################################################
#    Geometry
################################################################
screwPositiveRotations=True # ie rotation(axis,angle) "screws" when one looks  towards the axis and 
# the graphical representation in 3D has x on right, y in front and z up.  
################################################################
#    Lights and colors
################################################################
defaultLightType="" # . By default, a usual pointlight defined by the empty string.  Spotlight is possible

# Ambient ligth : so that objects are visible even if you don't add lights in your scene. Gives no shadow. Gives ligth on
# every part of your object. Similar to a diffuse ligth in a room
defaultAmbientRgb=[0.507,0.507,.507] # rgb colors of the ambient light
defaultAmbientRgbIntensity=1.2 # intensity=multiplier for the above rgb colors

## Some lights give shadow and some don't. Values by default for these lights. 
# lights with shadow 
shadowlightDefaultRgb=[.522,.522,.522]
defaultShadowlightRgbIntensity=.8# intensity=multiplier for the above rgb colors
# lights without shadow
shadowlesslightDefaultRgb=[.322,.322,.322]
defaultShadowlesslightRgbIntensity=.6# intensity=multiplier for the above rgb colors
# usual solid objects
defaultRgb=[.25,.25,0]
defaultRgbIntensity=1
defaultDiffuseMultiplier=.6
defaultAmbientMultiplier=.15
