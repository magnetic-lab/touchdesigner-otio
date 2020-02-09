import td

from .tdotioentity import TDOtioEntity
from .tdotiostack import TDOtioStack


class TDOtioTimeline(TDOtioEntity):

    def __init__(self, parent, otio_timeline):
        self.owner_comp = parent.create(td.containerCOMP, "timeline")
        self.otio = otio_timeline
        self.type = "video"  # TODO: make Enum
        self.video_stack = TDOtioStack(self.owner_comp, self.otio.video_tracks())
        self.build()

    @property
    def name(self):
        return self.owner_comp.name

    def build(self):

        for op_ in self.video_stack.owner_comp.findChildren(type=td.containerCOMP):
            op_.destroy()
