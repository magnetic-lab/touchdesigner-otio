import td
from .tdotiotrack import TDOtioTrack


class TDOtioTimeline:

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

        for track in self.otio.video_tracks():
            if not len(track):
                continue
            tdotio_t = TDOtioTrack(track, stack)
            tdotio_t.ownerComp.par.alignorder = len(self.tracks)
            self.tracks.append(tdotio_t)
