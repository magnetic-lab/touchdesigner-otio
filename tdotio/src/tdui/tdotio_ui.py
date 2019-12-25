import os
import sys

import opentimelineio as otio

TDOTIO_PATH = os.path.join(os.environ.get("TDOTIO_PATH", ""), "src", "tdui")
if TDOTIO_PATH and not TDOTIO_PATH in sys.path:
    sys.path.append(TDOTIO_PATH)

from tdotiotimeline_ui import TDOtioTimelineUI

TEST_FCPXML = "E:\\SANDBOX\\tdotio_demo\\tdotio_demo.xml"


class TDOtioUI:

    def __init__(self, ownerComp):

        self.ownerComp = ownerComp
        self.core = self.ownerComp.op("tdotio_core")
        self._current_frame = self.core.op("null_playhead")[0]
        self.timeline = self.read_from_file(TEST_FCPXML)

        self.__build()

    @property
    def Name(self):
        return self.ownerComp.name

    def read_from_file(self, target_file):
        garbage = self.ownerComp.op("timeline/video").children
        try:
            self.timeline = TDOtioTimelineUI(
                otio.adapters.read_from_file(target_file), self.ownerComp)

            for child in garbage:
                child.destroy()
        except:
            print(str(target_file))
            raise

        return self.timeline

    def ReadFromFile(self, *args, **kwargs):
        """Touch Designer Wrapper method for 'read_from_file'."""
        return self.read_from_file(*args, **kwargs)

    def Timeline(self):
        return self.timeline

    def Core(self):
        return self.core

    def play(self):
        first = None
        second = None
        next_ = None

        for track in self.timeline.otio.video_tracks():
            start_time = track.visible_range().start_time.value
            duration = track.visible_range().duration.value

            if start_time <= self._current_frame <= start_time + duration:
                for clip in track:
                    if not clip.schema_name() == "Clip":
                        continue
                    c_start_time = clip.trimmed_range_in_parent().start_time.value
                    c_duration = clip.trimmed_range_in_parent().duration.value
                    if not c_start_time <= self._current_frame <= c_start_time + c_duration:
                        continue

                    if not first:
                        first = clip
                    else:
                        second = clip

            if first and second:
                break

        # find next clip to be loaded into buffer

        return first.name if first else first, second.name if second else second, next_

    def Play(self):
        return self.play()

    def __build(self):

        self.core.op("slider_timeline").par.Valuerange2 = self.timeline.otio.duration().value
