import weakref
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

from PySide2 import (
    QtGui,
    QtWidgets,
    QtCore,
)  # https://github.com/mottosso/Qt.py by Marcus Ottosson


def dock_window(dialog_class):
    try:
        cmds.deleteUI(dialog_class.CONTROL_NAME)
        logger.info("removed workspace {}".format(dialog_class.CONTROL_NAME))

    except:
        pass

    # building the workspace control with maya.cmds
    main_control = cmds.workspaceControl(
        dialog_class.CONTROL_NAME,
        dtm=["right", True],
        iw=300,
        mw=True,
        wp="preferred",
        label=dialog_class.DOCK_LABEL_NAME,
    )

    # now lets get a C++ pointer to it using OpenMaya
    control_widget = omui.MQtUtil.findControl(dialog_class.CONTROL_NAME)
    # convert the C++ pointer to Qt object we can use
    control_wrap = wrapInstance(int(control_widget), QtWidgets.QWidget)

    # control_wrap is the widget of the docking window and now we can start working with it:
    control_wrap.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    win = dialog_class(control_wrap)

    # after maya is ready we should restore the window since it may not be visible
    cmds.evalDeferred(
        lambda *args: cmds.workspaceControl(main_control, e=True, rs=True)
    )

    # will return the class of the dock content.
    return win.run()


class DockableGUI(QtWidgets.QWidget):
    instances = list()
    CONTROL_NAME = "dockable_gui_test"
    DOCK_LABEL_NAME = "Dockable GUI test"

    def __init__(self, parent=None):
        super(DockableGUI, self).__init__(parent)

        # let's keep track of our docks so we only have one at a time.
        DockableGUI.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))

        self.window_name = self.CONTROL_NAME
        self.ui = parent
        self.main_layout = parent.layout()

        # here we can start coding our UI
        # lets add 25 line_edits and 4 buttons LOL :>
        for i in range(0, 25):
            self.dynamiclineedit = QtWidgets.QLineEdit(self)
            self.dynamiclineedit.setText("Text goes here")
            self.main_layout.addWidget(self.dynamiclineedit)

        for i in range(0, 5):
            self.button = QtWidgets.QPushButton(self)
            self.button.setText("Click Here")
            self.main_layout.addWidget(self.button)

    @staticmethod
    def delete_instances():
        for ins in DockableGUI.instances:
            logger.info("Delete {}".format(ins))
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass

            DockableGUI.instances.remove(ins)
            del ins

    def run(self):
        return self


# this is where we call the window
my_dock = dock_window(DockableGUI)
