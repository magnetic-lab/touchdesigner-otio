import td

class TDOtioClipUI:

	def __init__(self, otio_clip, parent):
		self.ownerComp = parent.create(td.containerCOMP, otio_clip.name)
		self.otio = otio_clip