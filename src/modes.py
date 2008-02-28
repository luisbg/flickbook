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
    def __init__(self, timeline, fps, image):
        self.timeOpA = clutter.Timeline(150, fps)
        self.timeOpB = clutter.Timeline(50, fps)
        self.cin1 = timeline.connect("started", self.timeOpA_start)
        self.cin2 = self.timeOpA.connect("completed", self.timeOpB_start)

        alphaDepth = clutter.Alpha(timeline, clutter.ramp_inc_func)
        self.depth = clutter.BehaviourDepth(alphaDepth, 0, 100)
        alphaOpacity = clutter.Alpha(self.timeOpA, clutter.sine_inc_func)
        self.opacityUp = clutter.BehaviourOpacity(alphaOpacity, 0, 255)
        alphaOpacity = clutter.Alpha(self.timeOpB, clutter.sine_inc_func)
        self.opacityDown = clutter.BehaviourOpacity(alphaOpacity, 255, 0)

        self.depth.apply(image)
        self.opacityUp.apply(image)
        self.opacityDown.apply(image)

    def timeOpA_start(self, data):
        self.timeOpA.start()
        self.timeOpB.rewind()

    def timeOpB_start(self, data):
        self.timeOpA.rewind()
        self.timeOpB.start()

    def set_speed(self, fps):
        self.timeOpA.set_speed(fps)
        self.timeOpB.set_speed(fps)

    def disconnect(self, timeline):
        timeline.disconnect(self.cin1)
        self.timeOpA.disconnect(self.cin2)

class Rotate():
    def __init__(self, timeline, fps, image):
        self.timeOpA = clutter.Timeline(50, fps)
        self.timeOpB = clutter.Timeline(150, fps)
        self.cin1 = timeline.connect("started", self.timeOpA_start)
        self.cin2 = self.timeOpA.connect("completed", self.timeOpB_start)

        alphaDepth = clutter.Alpha(timeline, clutter.ramp_inc_func)
        self.depth = clutter.BehaviourDepth(alphaDepth, 40, 0)
        alphaOpacity = clutter.Alpha(self.timeOpA, clutter.sine_inc_func)
        self.opacityUp = clutter.BehaviourOpacity(alphaOpacity, 0, 255)
        alphaOpacity = clutter.Alpha(self.timeOpB, clutter.sine_inc_func)
        self.opacityDown = clutter.BehaviourOpacity(alphaOpacity, 255, 0)
        alphaRotate = clutter.Alpha(timeline, clutter.smoothstep_inc_func)
        self.rotate = clutter.BehaviourRotate(alphaRotate, 0, 1)
        self.rotate.set_property("angle-end", 350)
 
        self.depth.apply(image)
        self.rotate.apply(image)
        self.opacityUp.apply(image)
        self.opacityDown.apply(image)

    def timeOpA_start(self, data):
        self.timeOpA.start()
        self.timeOpB.rewind()

    def timeOpB_start(self, data):
        self.timeOpA.rewind()
        self.timeOpB.start()

    def set_speed(self, fps):
        self.timeOpA.set_speed(fps)
        self.timeOpB.set_speed(fps)

    def disconnect(self, timeline):
        timeline.disconnect(self.cin1)
        self.timeOpA.disconnect(self.cin2)

class Scroll():
    def __init__(self, timeline, fps, image, x_pos):
        self.timeOpA = clutter.Timeline(150, fps)
        self.timeOpB = clutter.Timeline(50, fps)
        self.cin1 = timeline.connect("started", self.timeOpA_start)
        self.cin2 = self.timeOpA.connect("completed", self.timeOpB_start)

        alphaOpacity = clutter.Alpha(self.timeOpA, clutter.sine_inc_func)
        self.opacityUp = clutter.BehaviourOpacity(alphaOpacity, 0, 255)
        alphaOpacity = clutter.Alpha(self.timeOpB, clutter.sine_inc_func)
        self.opacityDown = clutter.BehaviourOpacity(alphaOpacity, 255, 0)

        knots = ( \
                ( x_pos, -100 ),   \
                ( x_pos,  200 ),   \
        )

        alpha = clutter.Alpha(timeline, clutter.ramp_inc_func)
        self.path = clutter.BehaviourPath(alpha=alpha, knots=knots)
        
        self.path.apply(image)
        self.opacityUp.apply(image)
        self.opacityDown.apply(image)

    def timeOpA_start(self, data):
        self.timeOpA.start()
        self.timeOpB.rewind()

    def timeOpB_start(self, data):
        self.timeOpA.rewind()
        self.timeOpB.start()

    def set_speed(self, fps):
        self.timeOpA.set_speed(fps)
        self.timeOpB.set_speed(fps)

    def disconnect(self, timeline):
        timeline.disconnect(self.cin1)
        self.timeOpA.disconnect(self.cin2)
