import td

from .tdotioentity import TDOtioEntity
from .tdotiotrack import TDOtioTrack


class TDOtioStack(TDOtioEntity):

    def __init__(self, parent, tracks_list):
        # TODO: the name here should be inherited more dynamically (in case its for audio)
        self.owner_comp = parent.create(td.containerCOMP, "video")
        self.otio = tracks_list
        self.tracks = []

        self.__build()

    def Build(self):
        self.__build()

    def __build(self):
        self.__cleanup()
        y_offset = 5
        ypos = None
        stack_w = 0
        stack_h = 0

        for otio_track in self.otio:
            tdotio_track = TDOtioTrack(self.owner_comp, otio_track)
            self.tracks.append(tdotio_track)

            # set track container positions so they stack visually in the node graph
            if ypos is None:
                ypos = tdotio_track.owner_comp.nodeY
            else:
                ypos = ypos - tdotio_track.owner_comp.nodeHeight - y_offset
                tdotio_track.owner_comp.nodeY = ypos

            # set their align order for correct ordering in TD ui
            tdotio_track.owner_comp.par.alignorder = self.otio.index(otio_track)

            # set stack width to the highest track width
            if tdotio_track.owner_comp.par.w > stack_w:
                stack_w = tdotio_track.owner_comp.par.w
            stack_h += tdotio_track.owner_comp.par.h

        self.owner_comp.par.w = stack_w
        self.owner_comp.par.h = stack_h
        self.owner_comp.par.align = 4  # 4: `Bottom To Top`

    def __cleanup(self):
        for op_ in self.owner_comp.children:
            text_ext_name = "text_" + self.__class__.__name__ + "Ext"  # text_TDOtioStackExt
            if op_.name == text_ext_name:
                continue

            op_.destroy()
