import td

from .tdotioentity import TDOtioEntity
from .tdotioclip import TDOtioClip


class TDOtioTrack(TDOtioEntity):

    TRACK_HEIGHT = 75

    def __init__(self, parent, otio_track):
        self.name = otio_track.name or "track"
        self.owner_comp = parent.create(td.containerCOMP, self.make_legal(self.name))
        self.otio = list(otio_track)
        self.clips = []
        self.__build()

    def __build(self):
        self.owner_comp.par.h = self.TRACK_HEIGHT  # have to set here before creating clips

        for clip in list(self.otio):
            tdotio_c = TDOtioClip(self.owner_comp, clip)
            if not self.clips:
                self.clips.append(tdotio_c)
                tdotio_c.owner_comp.nodeWidth = tdotio_c.owner_comp.par.w
                continue

            prev = self.clips[-1]
            # set the x to be previous' x + w
            xpos = prev.owner_comp.par.x + prev.owner_comp.par.w
            tdotio_c.owner_comp.par.x = xpos
            tdotio_c.owner_comp.nodeX = xpos
            tdotio_c.owner_comp.nodeWidth = tdotio_c.owner_comp.par.w
            self.clips.append(tdotio_c)

        # make sure the total width is equal to the last clip's x + w
        if self.clips:
            self.owner_comp.par.w = self.clips[-1].owner_comp.par.x + \
                self.clips[-1].owner_comp.par.w
