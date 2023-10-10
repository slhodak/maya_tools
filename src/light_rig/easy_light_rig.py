import maya.cmds as cmds


# Get the parent of the light using listRelatives
def get_spotlight_parent(spot_light):
    spot_light_parent = cmds.listRelatives(spot_light, parent=True)
    if spot_light_parent:
        return spot_light_parent[0]


def create_easy_light_rig():
    # Create a point light for the key light
    key_light = cmds.spotLight(name="key_light")
    key_light_parent = get_spotlight_parent(key_light)

    cmds.setAttr(key_light_parent + ".translateX", 5)
    cmds.setAttr(key_light_parent + ".translateY", 0)
    cmds.setAttr(key_light_parent + ".translateZ", 5)
    cmds.setAttr(key_light_parent + ".rotateY", 35)

    # Create a spot light for the fill light
    fill_light = cmds.spotLight(name="fill_light")
    fill_light_parent = get_spotlight_parent(fill_light)

    cmds.setAttr(fill_light_parent + ".translateX", -5)
    cmds.setAttr(fill_light_parent + ".translateY", 0)
    cmds.setAttr(fill_light_parent + ".translateZ", 5)
    cmds.setAttr(fill_light_parent + ".rotateY", -45)

    # Create a directional light for the backlight
    back_light = cmds.spotLight(name="back_light")
    back_light_parent = get_spotlight_parent(back_light)

    cmds.setAttr(back_light_parent + ".translateX", 0)
    cmds.setAttr(back_light_parent + ".translateY", 5)
    cmds.setAttr(back_light_parent + ".translateZ", -5)
    cmds.setAttr(back_light_parent + ".rotateY", 180)
    cmds.setAttr(back_light_parent + ".rotateX", -30)

    cmds.setAttr(key_light + ".aiExposure", 8)
    cmds.setAttr(fill_light + ".aiExposure", 6)
    cmds.setAttr(back_light + ".aiExposure", 8)

    # Group all lights under a parent group
    light_group = cmds.group(key_light, fill_light, back_light, name="light_rig")

    # Create a camera
    render_cam = cmds.camera(name="renderCam")
    render_cam_transform = render_cam[0]
    cmds.setAttr(render_cam_transform + ".translateZ", 7.5)
