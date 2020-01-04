class TDOtioStack:
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.__comp_stack = self.ownerComp.op("comp_stack")

	def build(self, tracks_list):
		y_offset = 5
		ypos = None
		for track in tracks_list:
			index = tracks_list.index(track)
			mvit = self.ownerComp.create(
				moviefileinTOP, "{0}_{1}".format(index, track.name))
			if ypos is None:
				ypos = mvit.nodeY
			else:
				mvit.nodeY = ypos - mvit.nodeHeight - y_offset
			self.__comp_stack.inputConnectors[index].connect(mvit)

