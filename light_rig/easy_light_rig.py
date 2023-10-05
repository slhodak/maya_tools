import maya.cmds as cmds

# Create a point light for the key light
key_light = cmds.spotLight(name="key_light")
# Get the parent of the key_light using listRelatives
key_light_parent = cmds.listRelatives(key_light, parent=True)
if key_light_parent:
    key_light_parent = key_light_parent[0]

cmds.setAttr(key_light_parent + ".translateX", 5)
cmds.setAttr(key_light_parent + ".translateY", 0)
cmds.setAttr(key_light_parent + ".translateZ", 5)
cmds.setAttr(key_light_parent + ".rotateY", 35)

# Create a spot light for the fill light
fill_light = cmds.spotLight(name="fill_light")
# Get the parent of the key_light using listRelatives
fill_light_parent = cmds.listRelatives(fill_light, parent=True)
if fill_light_parent:
    fill_light_parent = fill_light_parent[0]
cmds.setAttr(fill_light_parent + ".translateX", -5)
cmds.setAttr(fill_light_parent + ".translateY", 0)
cmds.setAttr(fill_light_parent + ".translateZ", 5)
cmds.setAttr(fill_light_parent + ".rotateY", -45)

# Create a directional light for the backlight
back_light = cmds.spotLight(name="back_light")
# Get the parent of the key_light using listRelatives
back_light_parent = cmds.listRelatives(back_light, parent=True)
if back_light_parent:
    back_light_parent = back_light_parent[0]
cmds.setAttr(back_light_parent + ".translateX", 0)
cmds.setAttr(back_light_parent + ".translateY", 5)
cmds.setAttr(back_light_parent + ".translateZ", -5)
cmds.setAttr(back_light_parent + ".rotateY", 180)
cmds.setAttr(back_light_parent + ".rotateX", -30)

# Group all lights under a parent group
light_group = cmds.group(key_light, fill_light, back_light, name="light_rig")

cmds.setAttr(key_light + ".aiExposure", 8)
cmds.setAttr(fill_light + ".aiExposure", 6)
cmds.setAttr(back_light + ".aiExposure", 8)

# Create a camera
render_cam = cmds.camera(name="renderCam")
render_cam_transform = render_cam[0]
cmds.setAttr(render_cam_transform + ".translateZ", 7.5)
