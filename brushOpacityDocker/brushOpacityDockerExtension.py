from krita import *
from PyQt5 import QtCore

class BrushOpacityDockerExtension(Extension):

    SIGNAL_CYCLE = QtCore.pyqtSignal()

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        pass
        
    def createActions(self, window):
        action = window.createAction("cycleBrushOpacity", "Next brush opacity", "tools/scripts")
        action.triggered.connect(self.cycleBrushOpacity)

    def cycleBrushOpacity(self):
        self.SIGNAL_CYCLE.emit()

# And add the extension to Krita's list of extensions:
# Krita.instance().addExtension(MyExtension(Krita.instance()))