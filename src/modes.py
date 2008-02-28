#!/usr/bin/python
#
#  Copyright Luis de Bethencourt Guimera, Andrew Hunter 2008
#
#    This program is free software; you may redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by the Free 
#    Software Foundation; either version 2 of the License, or (at your option) 
#    any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
#    more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import clutter

class Slideshow():
    def __init__(self, timeline, image):
        alphaDepth = clutter.Alpha(timeline, clutter.ramp_inc_func)
        self.depth = clutter.BehaviourDepth(alphaDepth, 0, 100)
        alphaOpacity = clutter.Alpha(timeline, clutter.sine_inc_func)
        self.opacity = clutter.BehaviourOpacity(alphaOpacity, 0, 255)
 
        self.depth.apply(image)
        self.opacity.apply(image)

class Test():
    def __init__(self, timeline, image):
        alphaDepth = clutter.Alpha(timeline, clutter.ramp_inc_func)
        self.depth = clutter.BehaviourDepth(alphaDepth, 0, 200)
        alphaOpacity = clutter.Alpha(timeline, clutter.sine_inc_func)
        self.opacity = clutter.BehaviourOpacity(alphaOpacity, 0, 255)
        alphaRotate = clutter.Alpha(timeline, clutter.smoothstep_inc_func)
        self.rotate = clutter.BehaviourRotate(alphaRotate, 1, 0)
        self.rotate.set_property("angle-end", 240)
 
        self.depth.apply(image)
        self.opacity.apply(image)
        self.rotate.apply(image)
