import td
from .tdotioclip import TDOtioClip


class TDOtioTrack:

    TRACK_HEIGHT = 75

    def __init__(self, otio_track, parent):
        self.name = otio_track.name or "track"
        self.ownerComp = parent.create(td.containerCOMP, self.name)
        self.otio = list(otio_track)
        self.clips = []

        self.__build()

    def __build(self):
        self.ownerComp.par.h = self.TRACK_HEIGHT  # have to set here before creating clips

        for clip in list(self.otio):
            tdotio_c = TDOtioClip(clip, self.ownerComp)

            if not self.clips:
                self.clips.append(tdotio_c)
                continue

            prev = self.clips[-1]
            # set the x to be previous' x + w
            tdotio_c.ownerComp.par.x = prev.ownerComp.par.x + prev.ownerComp.par.w
            self.clips.append(tdotio_c)

        # make sure the total width is equal to the last clip's x + w
        if self.clips:
            self.ownerComp.par.w = self.clips[-1].ownerComp.par.x + self.clips[-1].ownerComp.par.w
