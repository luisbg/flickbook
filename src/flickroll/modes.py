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
import random

class Slideshow():
    def __init__(self, timeline, fps, image):
        self.timeOp_black = clutter.Timeline(5, fps)
        self.timeOpUp = clutter.Timeline(150, fps)
        self.timeOpDown = clutter.Timeline(45, fps)
        self.cin = timeline.connect("started", self.timeOp_black_start, image)
        self.cinUp = self.timeOp_black.connect("completed", self.timeOpUp_start, image)
        self.cinDown = self.timeOpUp.connect("completed", self.timeOpDown_start, image)

        alphaDepth = clutter.Alpha(timeline, clutter.ramp_inc_func)
        self.depth = clutter.BehaviourDepth(alphaDepth, 0, 100)
        alphaOpacity = clutter.Alpha(self.timeOpUp, clutter.sine_inc_func)
        self.opacityUp = clutter.BehaviourOpacity(alphaOpacity, 0, 255)
        alphaOpacity = clutter.Alpha(self.timeOpDown, clutter.sine_inc_func)
        self.opacityDown = clutter.BehaviourOpacity(alphaOpacity, 255, 0)

        self.opacityUp.apply(image)
        self.opacityDown.apply(image)
        self.depth.apply(image)

    def timeOp_black_start(self, data, image): 
        image.hide()
        self.timeOp_black.start()

    def timeOpUp_start(self, data, image):
        image.show()
        self.timeOpUp.start()
        self.timeOpDown.rewind()

    def timeOpDown_start(self, data, image):
        self.timeOpUp.rewind()
        self.timeOpDown.start()

    def set_speed(self, fps):
        self.timeOpUp.set_speed(fps)
        self.timeOpDown.set_speed(fps)

    def disconnect(self, timeline):
        timeline.disconnect(self.cin)
        self.timeOp_black.disconnect(self.cinUp)
        self.timeOpUp.disconnect(self.cinDown)

class Rotate():
    def __init__(self, timeline, fps, image):
        self.timeOp_black = clutter.Timeline(5, fps)
        self.timeOpA = clutter.Timeline(180, fps)
        self.timeOpB = clutter.Timeline(15, fps)
        self.cin = timeline.connect("started", self.timeOp_black_start, image)
        self.cin1 = self.timeOp_black.connect("completed", self.timeOpA_start, image)
        self.cin2 = self.timeOpA.connect("completed", self.timeOpB_start)

        alphaDepth = clutter.Alpha(timeline, clutter.ramp_inc_func)
        self.depth = clutter.BehaviourDepth(alphaDepth, -1000, 10)
        alphaOpacity = clutter.Alpha(self.timeOpA, clutter.sine_inc_func)
        self.opacityUp = clutter.BehaviourOpacity(alphaOpacity, 0, 255)
        alphaOpacity = clutter.Alpha(self.timeOpB, clutter.sine_inc_func)
        self.opacityDown = clutter.BehaviourOpacity(alphaOpacity, 255, 0)
        alphaRotate = clutter.Alpha(timeline, clutter.smoothstep_inc_func)
        self.rotate = clutter.BehaviourRotate(alphaRotate, 0, 0)
        self.rotate.set_property("angle-end", 30)
 
        self.depth.apply(image)
        self.rotate.apply(image)
        self.opacityUp.apply(image)
        self.opacityDown.apply(image)

    def timeOp_black_start(self, data, image): 
        image.hide()
        self.timeOp_black.start()

    def timeOpA_start(self, data, image):
        image.show()
        self.timeOpA.start()
        self.timeOpB.rewind()

    def timeOpB_start(self, data):
        self.timeOpA.rewind()
        self.timeOpB.start()

    def set_speed(self, fps):
        self.timeOpA.set_speed(fps)
        self.timeOpB.set_speed(fps)

    def disconnect(self, timeline):
        timeline.disconnect(self.cin)
        self.timeOp_black.disconnect(self.cin1)
        self.timeOpA.disconnect(self.cin2)

class Scroll():
    def __init__(self, timeline, fps, image, x_pos):
        self.timeOp_black = clutter.Timeline(5, fps)
        self.timeOpA = clutter.Timeline(150, fps)
        self.timeOpB = clutter.Timeline(45, fps)
        self.cin = timeline.connect("started", self.timeOp_black_start, image)
        self.cin1 = self.timeOp_black.connect("completed", self.timeOpA_start, image)
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
    
    def timeOp_black_start(self, data, image):
        image.hide()
        self.timeOp_black.start()

    def timeOpA_start(self, data, image):
        image.show()
        self.timeOpA.start()
        self.timeOpB.rewind()

    def timeOpB_start(self, data):
        self.timeOpA.rewind()
        self.timeOpB.start()

    def set_speed(self, fps):
        self.timeOpA.set_speed(fps)
        self.timeOpB.set_speed(fps)

    def disconnect(self, timeline):
        timeline.disconnect(self.cin)
        self.timeOp_black.disconnect(self.cin1)
        self.timeOpA.disconnect(self.cin2)

class SlideText():
    def __init__(self, timeline, fps, image, label):
        f = open('../files/english', 'r')
        self.lines = f.readlines()

        c = 0
        while c < len(self.lines):
            self.lines[c] = self.lines[c][:-1]
            c += 1

        self.label = label
        self.label.set_text(self.lines[random.randint(0, len(self.lines) -1)])
        self.label.set_position(random.randint(0, 600), random.randint(0, 400))
        self.label.set_color(clutter.Color(200, 200, 200))
        self.label.set_opacity(0)

        self.timeOp_black = clutter.Timeline(5, fps)
        self.timeOpA = clutter.Timeline(150, fps)
        self.timeOpB = clutter.Timeline(45, fps)
        self.cin = timeline.connect("started", self.timeOp_black_start, image)
        self.cin1 = self.timeOp_black.connect("completed", self.timeline_start, image)
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

        self.timeline = clutter.Timeline(200, fps)
        self.cin_label = timeline.connect("started", self.timeline_start, image)

        alphaOpacity = clutter.Alpha(self.timeline, clutter.ramp_inc_func)
        self.opacity = clutter.BehaviourOpacity(alphaOpacity, 0, 255)

        self.opacity.apply(self.label)

    def timeOp_black_start(self, data, image):
        image.hide()
        self.timeOp_black.start()

    def timeline_start(self, data, image):
        image.show()
        self.label.set_text(self.lines[random.randint(0, len(self.lines) -1)])
        self.label.set_opacity(0)
        self.label.set_position(random.randint(0, 600), random.randint(0, 400))

        self.timeOpA.start()
        self.timeOpB.rewind()

        self.timeline.rewind()
        self.timeline.start()

    def timeOpB_start(self, data):
        self.timeOpA.rewind()
        self.timeOpB.start()

    def set_speed(self, fps):
        self.timeline.set_speed(fps)
        self.timeOpA.set_speed(fps)
        self.timeOpB.set_speed(fps)

    def disconnect(self, timeline):
        timeline.disconnect(self.cin)
        self.timeOp_black.disconnect(self.cin1)
        self.timeOpA.disconnect(self.cin2)
        timeline.disconnect(self.cin_label)
