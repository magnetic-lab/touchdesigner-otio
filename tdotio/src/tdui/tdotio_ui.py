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
                if not child.__class__.__name__ == "containerCOMP":
                    continue
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
        a_media = None
        b_media = None
        next_ = None

        reversed_tracks = list(self.timeline.otio.video_tracks())
        reversed_tracks.reverse()
        for track in reversed_tracks:
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

                    if not a_media:
                        a_media = clip
                    else:
                        b_media = clip

            if a_media and b_media:
                break

        # find next clip to be loaded into buffer
        if a_media:
            self.core.op("moviefilein_a").par.file = self.__decode_url(
                a_media.media_reference.target_url)
            self.core.op("moviefilein_a").par.reloadpulse.pulse()
        if b_media:
            self.core.op("moviefilein_b").par.file = self.__decode_url(
                b_media.media_reference.target_url)
            self.core.op("moviefilein_b").par.reloadpulse.pulse()
        return a_media.name if a_media else a_media, b_media.name if b_media else b_media, next_

    def Play(self):
        return self.play()

    @staticmethod
    def __decode_url(url):
        return url.replace("file://localhost/", "").replace("%3a", ":")

    def __build(self):

        self.core.op("slider_timeline").par.Valuerange2 = self.timeline.otio.duration().value
