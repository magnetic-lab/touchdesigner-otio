import td

class TDOtioTimelineUI:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

	@property
	def name(self):
		return self.ownerComp.name
	