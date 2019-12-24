import random
import re

import td


class TDOtioClipUI:

    def __init__(self, otio_clip, parent):
        self.name = otio_clip.name or "clip"
        self.otio = otio_clip

        self.ownerComp = parent.create(td.containerCOMP, re.sub(r"\.|\s", "_", self.name))
        self.ownerComp.par.h = parent.par.h

        self.__core_base = self.ownerComp.create(td.baseCOMP, "core")

        self.__build()

    def start(self):
        return self.otio.visible_range().start_time.value

    def Start(self):
        return self.start()

    def duration(self):
        return self.otio.visible_range().duration.value

    def Duration(self):
        return self.duration()

    def __build(self):
        self.ownerComp.par.w = self.otio.duration().value

        # set a random bg-color for this containerCOMP
        rc = random.random(), random.random(), random.random()
        self.ownerComp.par.bgcolorr, self.ownerComp.par.bgcolorg, self.ownerComp.par.bgcolorb = rc
        self.ownerComp.par.bgalpha = 1

        # create 'core' base with textTOP for label
        label = self.__core_base.create(td.textTOP, "label")
        label.par.text = self.name
        label.par.resolutionw, label.par.resolutionh = self.ownerComp.par.w, self.ownerComp.par.h
        label.par.fontautosize = "fitiffat"
        self.ownerComp.par.top = label
