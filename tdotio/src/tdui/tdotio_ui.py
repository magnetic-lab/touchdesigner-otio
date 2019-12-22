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
        self.timeline = self.ReadFromFile(TEST_FCPXML)

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

    def ReadFromFile(self, *args, **kwargs):
        self.read_from_file(*args, **kwargs)
