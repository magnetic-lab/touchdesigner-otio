import os
import sys

import opentimelineio as otio

TDOTIO_PATH = os.path.join(os.environ.get("TDOTIO_PATH", ""), "src", "tdui")
if TDOTIO_PATH and not TDOTIO_PATH in sys.path:
	sys.path.append(TDOTIO_PATH)

from tdotiotimeline_ui import TDOtioTimelineUI

TEST_FCPXML = "D:\\premiere_projects\\test\\test_edit.xml"
class TDOtioUI:
	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.timeline = TDOtioTimelineUI(otio.adapters.read_from_file(TEST_FCPXML), self.ownerComp)

	@property
	def Name(self):
		return self.ownerComp.name
