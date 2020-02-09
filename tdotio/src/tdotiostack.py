import td

from .tdotioentity import TDOtioEntity
from .tdotiotrack import TDOtioTrack


class TDOtioStack(TDOtioEntity):

    def __init__(self, parent, tracks_list=None):
        # TODO: the name here should be inherited more dynamically (in case its for audio)
        self.owner_comp = parent.create(td.containerCOMP, "video")
        self.Tracks = [TDOtioTrack(self.owner_comp, track) for track in tracks_list] or []

        self.__build()

    def Build(self):
        self.__build()

    def __build(self):
        self.__reset()
        y_offset = 5
        ypos = None

        for track in self.Tracks:
            if ypos is None:
                ypos = track.owner_comp.nodeY
            else:
                track.owner_comp.nodeY = ypos - track.owner_comp.nodeHeight - y_offset
            # index = self.Tracks.index(track)
            # mfi_top = self.owner_comp.create(
            #     td.moviefileinTOP, "{0}_{1}".format(index, track.name))
            # if ypos is None:
            #     ypos = mfi_top.nodeY
            # else:
            #     mfi_top.nodeY = ypos - mfi_top.nodeHeight - y_offset
            # self._comp_stack.inputConnectors[index].connect(mfi_top)

    def __reset(self):
        for op_ in self.owner_comp.children:
            text_ext_name = "text_" + self.__class__.__name__ + "Ext"  # text_TDOtioStackExt
            if op_.name == text_ext_name:
                continue

            op_.destroy()
