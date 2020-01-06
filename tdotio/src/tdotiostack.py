import td


class TDOtioStack:

    def __init__(self, owner_comp):
        self.owner_comp = owner_comp
        self.__comp_stack = self.owner_comp.op("comp_stack")

    def __build(self, tracks_list):
        y_offset = 5
        ypos = None
        for track in tracks_list:
            index = tracks_list.index(track)
            mvit = self.owner_comp.create(
                td.moviefileinTOP, "{0}_{1}".format(index, track.name))
            if ypos is None:
                ypos = mvit.nodeY
            else:
                mvit.nodeY = ypos - mvit.nodeHeight - y_offset
            self.__comp_stack.inputConnectors[index].connect(mvit)

    def Build(self, tracks_list):
        self.__build(tracks_list)
