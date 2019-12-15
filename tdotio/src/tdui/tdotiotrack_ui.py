import td

from tdotioclip_ui import TDOtioClipUI


class TDOtioTrackUI:

	TRACK_HEIGHT = 75

	def __init__(self, otio_track, parent):
		self.ownerComp = parent.create(td.containerCOMP, otio_track.name)
		self.otio = list(otio_track)
		self.clips = []

	def __build(self):

		self.ownerComp.par.w = self.ownerComp.parent().par.w
		self.ownerComp.par.h = self.TRACK_HEIGHT

		for clip in list(self.otio):
			self.clips.append(TDOtioClipUI(clip, self.ownerComp))