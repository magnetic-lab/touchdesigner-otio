import random
import re

import td

from .tdotioentity import TDOtioEntity


class TDOtioClip(TDOtioEntity):

    def __init__(self, parent, otio_clip):
        self.name = otio_clip.name or "clip"
        self.otio = otio_clip
        self.owner_comp = parent.create(td.containerCOMP, self._make_legal(self.name))
        self.owner_comp.par.h = parent.par.h
        self._core_base = self.owner_comp.create(td.baseCOMP, "core")

        self.__build()

    def __build(self):
        self.owner_comp.par.w = self.otio.duration().value

        # set a random bg-color for this containerCOMP
        rc = random.random(), random.random(), random.random()
        self.owner_comp.par.bgcolorr, self.owner_comp.par.bgcolorg, self.owner_comp.par.bgcolorb = rc
        self.owner_comp.par.bgalpha = 1

        # create text_label
        label = self._core_base.create(td.textTOP, "label")
        label.par.text = self.name
        label.par.resolutionw, label.par.resolutionh = self.owner_comp.par.w, self.owner_comp.par.h
        label.par.fontautosize = "fitiffat"
        self.owner_comp.par.top = label

        if not self.is_media():
            return

    def is_media(self):
        # TODO: use otio api here
        return hasattr(self.otio, "media_reference")

    @property
    def duration(self):
        return self.otio.visible_range().duration.value

    @property
    def start(self):
        return self.otio.visible_range().start_time.value

    @property
    def path(self):
        return self._decode_url(self.otio.media_reference.target_url)
