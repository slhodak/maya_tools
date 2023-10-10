import os
from maya import cmds

USER_SCRIPT_DIR = os.path.abspath(cmds.internalVar(userScriptDir=True))

def get_icon_path(icon_name: str = ""):
    return os.path.join(USER_SCRIPT_DIR, f"maya_tools\img\{icon_name}")
