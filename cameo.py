#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import filters
from manager import CaptureManager, WindowManager
import rects
from trackers import FaceTracker

class Cameo(object):

	def __init__(self):
		self._windowManager = WindowManager('Cameo', self.onKeypress)
		self._captureManager = CaptureManager(cv2.VideoCapture(0),
			self._windowManager, True)
		self._faceTracker = FaceTracker()
		self._shouldDrawDebugRects = False
		self._curveFilter = filters.BGRPortraCurveFilter()

	def run(self):
		"""Run the main loop."""
		self._windowManager.createWindow()
		while self._windowManager.isWindowCreated:
			self._captureManager.enterFrame()
			frame = self._captureManager.frame

			# TODO: Filter the frame
			self._faceTracker.update(frame)
			faces = self._faceTracker.faces
			rects.swapRects(frame, frame,
				            [face.faceRect for face in faces])

			filters.strokeEdges(frame, frame)
			self._curveFilter.apply(frame, frame)

			if self._shouldDrawDebugRects:
				self._faceTracker.drawDebugRects(frame)

			self._captureManager.exitFrame()
			self._windowManager.processEvents()

	def onKeypress(self, keycode):
		"""Handle a keypress.
		space  -> Take a screenshot.
		tab    -> Start/stop recording a screencast.
		x      -> Start/stop drawing debug rectangles around faces.
		escape -> Quit.
		"""
		if keycode == 32:
			# space
			self._captureManager.writeImage('screenshot.png')
		elif keycode == 9:
			# tab
			if not self._captureManager.isWritingVideo:
				self._captureManager.startWritingVideo('screencast.avi')
			else:
				self._captureManager.stopWritingVideo()
		elif keycode == 120:
			self._shouldDrawDebugRects = \
				not self._shouldDrawDebugRects
		elif keycode == 27:
			# escape
			self._windowManager.destroyWindow()


if __name__ == "__main__":
	Cameo().run()
