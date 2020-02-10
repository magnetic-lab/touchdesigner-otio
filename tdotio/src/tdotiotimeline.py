import td

from .tdotioentity import TDOtioEntity
from .tdotiostack import TDOtioStack


class TDOtioTimeline(TDOtioEntity):

    def __init__(self, parent, otio_timeline):
        self.owner_comp = parent.create(td.containerCOMP, "timeline")
        self.otio = otio_timeline
        self.type = "video"  # TODO: make Enum
        self.video_stack = TDOtioStack(self.owner_comp, self.otio.video_tracks())

        self.__build()

    @property
    def name(self):
        return self.owner_comp.name

    def __build(self):
        self.owner_comp.nodeY = td.op.Core.nodeY + self.owner_comp.nodeHeight + 15
        self.owner_comp.nodeX = td.op.Core.nodeX
        self.owner_comp.par.w.expr = "parent().par.w"
        self.owner_comp.par.phscrollbar = 1
        self.owner_comp.par.h = td.op.Playhead.par.h = self.video_stack.owner_comp.par.h

        select_playhead = self.owner_comp.create(td.selectCOMP, "select_playhead")
        select_playhead.par.selectpanel = td.op.Playhead
        select_playhead.par.matchsize = 1
        select_playhead.par.layer = 10  # depth layer
        select_playhead.par.alignallow = 1  # 1: `Ignore`
        select_playhead.par.x.expr = "op('{0}')[0]".format(
            td.op.Core.op("null_current_frame").path)
