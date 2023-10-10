from maya import cmds


def setup():
    print("Running User Setup in maya/scripts")
    from maya_tools.src.create_shelf import add_or_update_custom_shelf

    add_or_update_custom_shelf()


cmds.scriptJob(event=["NewSceneOpened", setup])
