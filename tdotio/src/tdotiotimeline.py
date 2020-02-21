import td
import opentimelineio as otio

from .tdotioentity import TDOtioEntity
from .tdotiostack import TDOtioStack
from .tdotiotrack import TDOtioTrack


class TDOtioTimeline(TDOtioEntity):

    def __init__(self, parent, otio_timeline):
        self.owner_comp = parent.create(td.containerCOMP, "timeline")
        self.otio = otio_timeline
        self.type = "video"  # TODO: make Enum
        self.video_stack = TDOtioStack(self.owner_comp, self.otio.video_tracks())
        self.flattened_video_track = TDOtioTrack(
            self.owner_comp.create(td.baseCOMP, "flattened_video_track"), self.flatten())

        self.__current_clip = None
        self.__current_clip_end_frame = 0

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

    def flatten(self):
        print(otio.algorithms.flatten_stack(self.otio.video_tracks()))
        return otio.algorithms.flatten_stack(self.otio.video_tracks())

    def clip_at_frame(self, frame):
        # return early while frame is still on the same clip
        if self.__current_clip:
            start_frame = self.__current_clip_end_frame - self.__current_clip.duration().value
            if self.__current_clip_end_frame >= frame >= start_frame:
                return self.__current_clip

        # find which clip is at frame
        self.__current_clip_end_frame = 0
        for clip in list(self.flattened_video_track.otio):
            start_frame = self.__current_clip_end_frame
            self.__current_clip_end_frame += clip.duration().value
            print(clip)
            print(self.__current_clip_end_frame)

            # non-media clips
            # if not hasattr(clip, "media_reference"):
            #     self.__current_clip = None
            #     continue

            #
            if self.__current_clip_end_frame >= frame >= start_frame:
                print(clip)
                self.__current_clip = clip
                return self.__current_clip

        return self.__current_clip
