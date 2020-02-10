"""Touch Designer OpenTimelineIO implementation.

TDOtio is a tox which visualizes and plays back any otio-compatible timeline format within Touch.
TDOtio serves both as a visual interactive representation of a timeline and also a playback engine
with controls for reviewing content inside Touch Designer.

TODO: in the current implementation, only the topmost 2 tracks' media clips which simultaneosly
occupy the current playhead frame are loaded and displayed by 2 moviefileinTOP's. This means the
resulting output will not match the edit in Premiere in some cases. To resolve, we need to
dynamically create a new moviefileinTOP for each clip detected as being active and visible at the
current playhead(especially in cases involving transparency).
"""

import os
import sys

import opentimelineio as otio

TDOTIO_PATH = os.path.join(os.environ.get("TDOTIO_PATH", ""), "src")
if TDOTIO_PATH and not TDOTIO_PATH in sys.path:
    sys.path.append(TDOTIO_PATH)

from .tdotiotimeline import TDOtioTimeline

TEST_FCPXML = "E:\\SANDBOX\\tdotio_demo\\tdotio_demo.xml"


class TDOtio:

    def __init__(self, owner_comp):

        self.owner_comp = owner_comp
        self.core = self.owner_comp.op("tdotio_core")
        self._current_frame = self.core.op("null_playhead")[0]
        self.timeline = self.__read_from_file(TEST_FCPXML)

        self.__math_a_chop = self.core.op("math_a")
        self.__math_b_chop = self.core.op("math_b")
        self.__movie_a_top = self.core.op("moviefilein_a")
        self.__movie_b_top = self.core.op("moviefilein_b")
        self.__build()

    @property
    def Name(self):
        return self.owner_comp.name

    @staticmethod
    def __decode_url(url):
        return url.replace("file://localhost/", "").replace("%3a", ":")

    def Core(self):
        return self.core

    def Pause(self):
        self.__pause()

    def Play(self):
        self.__play()

    def ReadFromFile(self, *args, **kwargs):
        """Touch Designer Wrapper method for '__read_from_file'."""
        return self.__read_from_file(*args, **kwargs)

    @property
    def Timeline(self):
        return self.timeline

    def __build(self):

        self.core.op("slider_timeline").par.Valuerange2 = self.timeline.otio.duration().value

    def __calculate_clip_start_offset(self, otio_clip):
        timeline_start = self.core.op("slider_timeline").par.Valuerange1
        clip_start = otio_clip.trimmed_range_in_parent().start_time.value

        return timeline_start - clip_start

    def __pause(self):
        slider_timeline = self.core.op("slider_timeline")
        playback_signal = self.core.op("playback_signal")[0]
        slider_timeline.par.Value0 = \
            playback_signal / (slider_timeline.par.Valuerange2 - slider_timeline.par.Valuerange1)
        self.core.op("playback_speed").par.resetpulse.pulse()
        slider_timeline.par.Sliderignoreinteract = False
        self.core.op("playback_rate").par.value0 = 0

    def __play(self):
        self.core.op("slider_timeline").par.Sliderignoreinteract = True
        self.core.op("playback_rate").par.value0 = 60

    def __read_from_file(self, target_file):
        self.timeline = TDOtioTimeline(
            self.owner_comp, otio.adapters.read_from_file(target_file))

        return self.timeline

    def get_playback_clips(self):
        # TODO: heavy optomization needed, change name
        a_media = None
        b_media = None

        # iterate over the reversed list so we're always looking at the top-most layers first
        reversed_tracks = list(self.timeline.otio.video_tracks())
        reversed_tracks.reverse()
        for track in reversed_tracks:
            start_time = track.visible_range().start_time.value
            duration = track.visible_range().duration.value

            # only continue if the current track exists at the current playhead
            if start_time <= self._current_frame <= start_time + duration:
                for clip in track:
                        # skip gaps
                    if not clip.schema_name() == "Clip":
                        continue

                    # check to see if the current clip's duration intersects the curent playhead
                    c_start_time = clip.trimmed_range_in_parent().start_time.value
                    c_duration = clip.trimmed_range_in_parent().duration.value
                    if not c_start_time <= self._current_frame <= c_start_time + c_duration:
                        continue

                    # TODO: this sucks we need to move to a more dynamic movieFileInTOP per track
                    if not a_media:
                        a_media = clip
                    else:
                        b_media = clip

            if a_media and b_media:
                break

        # find next clip to be loaded into buffer
        if a_media:
            self.__math_a_chop.par.preoff = self.__calculate_clip_start_offset(a_media)
            self.__movie_a_top.par.file = self.__decode_url(a_media.media_reference.target_url)
            self.__movie_a_top.par.reloadpulse.pulse()
        if b_media:
            self.__math_b_chop.par.preoff = self.__calculate_clip_start_offset(b_media)
            self.__movie_b_top.par.file = self.__decode_url(b_media.media_reference.target_url)
            self.__movie_b_top.par.reloadpulse.pulse()
