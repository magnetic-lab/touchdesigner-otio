import os
import sys

import opentimelineio as otio

TDOTIO_PATH = os.path.join(os.environ.get("TDOTIO_PATH", ""), "src", "tdui")
if TDOTIO_PATH and not TDOTIO_PATH in sys.path:
	sys.path.append(TDOTIO_PATH)

from tdotiotimeline_ui import TDOtioTimelineUI
from tdotiotrack_ui import TDOtioTrackUI


class TDOtioUI:
	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.tracks = []
		self._timeline = otio.adapters.read_from_file("D:\\premiere_projects\\test\\test_edit.xml")
		self.__build()

	@property
	def Name(self):
		return self.ownerComp.name

	@property
	def Timeline(self):
		return self._timeline

	def __build(self):
		tc = self.ownerComp.op("timeline")
		stack = tc.op("stack_1")

		track_count = 0
		for track in self._timeline.tracks:
			self.tracks.append(TDOtioTrackUI(track, stack))
