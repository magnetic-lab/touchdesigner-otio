import random
import re

import td

class TDOtioClipUI:

	def __init__(self, otio_clip, parent):
		self.name = otio_clip.name or "clip"
		self.otio = otio_clip

		self.ownerComp = parent.create(td.containerCOMP, re.sub(r"\.|\s", "_", self.name))
		self.ownerComp.par.h = parent.par.h

		self.__build()

	def __build(self):
		self.ownerComp.par.w = self.otio.duration().value

		rc = random.random(), random.random(), random.random()
		self.ownerComp.par.bgcolorr, self.ownerComp.par.bgcolorg, self.ownerComp.par.bgcolorb = rc
		self.ownerComp.par.bgalpha = 1