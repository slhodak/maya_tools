import os
from maya import cmds

USER_SCRIPT_DIR = os.path.abspath(cmds.internalVar(userScriptDir=True))

DEFAULT_ICON = os.path.join(USER_SCRIPT_DIR, "maya_tools\img\cake2.png")
