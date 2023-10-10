from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def mayaWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class TestWindow(QtWidgets.QDialog):
    def __init__(self, parent=mayaWindow()):
        super(TestWindow, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.resize(400, 250)
        self.setWindowFlags(self.windowFlags() or QtCore.Qt.WindowStaysOnTopHint)


if __name__ == "__main__":
    d = TestWindow()
    d.show()

