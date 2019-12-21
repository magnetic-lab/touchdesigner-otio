import td
from tdotiotrack_ui import TDOtioTrackUI

class TDOtioTimelineUI:

	def __init__(self, otio_timeline, parent):
		self.ownerComp = parent.op("timeline")
		self.otio = otio_timeline
		self.tracks = []

		self.__build()

	@property
	def name(self):
		return self.ownerComp.name

	def __build(self):
		stack = self.ownerComp.op("video")

		for track in self.otio.tracks:
			if not len(track):
				continue
			tdotio_t = TDOtioTrackUI(track, stack)
			tdotio_t.ownerComp.par.alignorder = len(self.tracks)
			self.tracks.append(tdotio_t)
		