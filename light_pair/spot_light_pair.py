import maya.cmds as cmds
import time

# Create two spotlights and name them based on current Unix time
current_time_unix = int(time.time())
spotlight1_name = "spotlight_" + str(current_time_unix) + "_1"
spotlight2_name = "spotlight_" + str(current_time_unix) + "_2"
spotlight1 = cmds.spotLight(name=spotlight1_name)
spotlight2 = cmds.spotLight(name=spotlight2_name)

spotlight1_transform = cmds.listRelatives(spotlight1, parent=True)
if spotlight1_transform:
    spotlight1_transform = spotlight1_transform[0]

spotlight2_transform = cmds.listRelatives(spotlight2, parent=True)
if spotlight2_transform:
    spotlight2_transform = spotlight2_transform[0]

# Create float constant for spotlight scales
# Connect float constants to scale X, Y, and Z attributes of both spotlights
scale_fc = cmds.shadingNode(
    "floatConstant",
    asUtility=True,
    name="floatConstant_" + str(current_time_unix) + "_scale",
)

for scale_property in [".scaleX", ".scaleY", ".scaleZ"]:
    cmds.connectAttr(scale_fc + ".outFloat", spotlight1_transform + scale_property)
    cmds.connectAttr(scale_fc + ".outFloat", spotlight2_transform + scale_property)

# Create float constants for radius
radius_fc = cmds.shadingNode(
    "floatConstant",
    asUtility=True,
    name="floatConstant_" + str(current_time_unix) + "_radius",
)

# Connect float constants to radius attributes of both spotlights
cmds.connectAttr(radius_fc + ".outFloat", spotlight1 + ".aiRadius")
cmds.connectAttr(radius_fc + ".outFloat", spotlight2 + ".aiRadius")

# Create float constants for cone angle
cone_angle_fc = cmds.shadingNode(
    "floatConstant",
    asUtility=True,
    name="floatConstant_" + str(current_time_unix) + "_cone_angle",
)
cmds.setAttr(cone_angle_fc + ".inFloat", 20)

# Connect float constants to cone angle attributes of both spotlights
cmds.connectAttr(cone_angle_fc + ".outFloat", spotlight1 + ".coneAngle")
cmds.connectAttr(cone_angle_fc + ".outFloat", spotlight2 + ".coneAngle")

# Create float constants for penumbra angle
penumbra_angle_fc = cmds.shadingNode(
    "floatConstant",
    asUtility=True,
    name="floatConstant_" + str(current_time_unix) + "_penumbra_angle",
)
cmds.setAttr(penumbra_angle_fc + ".inFloat", 0)

# Connect float constants to penumbra angle attributes of both spotlights
cmds.connectAttr(penumbra_angle_fc + ".outFloat", spotlight1 + ".penumbraAngle")
cmds.connectAttr(penumbra_angle_fc + ".outFloat", spotlight2 + ".penumbraAngle")

# Create float constants for color temperature
color_temp_fc = cmds.shadingNode(
    "floatConstant",
    asUtility=True,
    name="floatConstant_" + str(current_time_unix) + "_temp",
)
cmds.setAttr(color_temp_fc + ".inFloat", 5500)

# Connect float constants to color temperature attributes of both spotlights
cmds.connectAttr(color_temp_fc + ".outFloat", spotlight1 + ".aiColorTemperature")
cmds.connectAttr(color_temp_fc + ".outFloat", spotlight2 + ".aiColorTemperature")

# Create float constants for useColorTemperature
use_color_temp_fc = cmds.shadingNode(
    "floatConstant",
    asUtility=True,
    name="floatConstant_" + str(current_time_unix) + "_useTemp",
)
cmds.setAttr(use_color_temp_fc + ".inFloat", 1)

# Connect float constants to useColorTemperature attributes of both spotlights
cmds.connectAttr(use_color_temp_fc + ".outFloat", spotlight1 + ".aiUseColorTemperature")
cmds.connectAttr(use_color_temp_fc + ".outFloat", spotlight2 + ".aiUseColorTemperature")

# Create float constant for exposure
exposure_fc = cmds.shadingNode(
    "floatConstant",
    asUtility=True,
    name="floatConstant_" + str(current_time_unix) + "_exposure",
)
cmds.setAttr(exposure_fc + ".inFloat", 8)

# Connect float constants to exposure attributes of both spotlights
cmds.connectAttr(exposure_fc + ".outFloat", spotlight1 + ".aiExposure")
cmds.connectAttr(exposure_fc + ".outFloat", spotlight2 + ".aiExposure")

# Create a color constant
color_constant = cmds.shadingNode(
    "colorConstant",
    asUtility=True,
    name="colorConstant_" + str(current_time_unix) + "_color",
)

# Connect color constant to color attributes of both spotlights
cmds.connectAttr(color_constant + ".outColor", spotlight1 + ".color")
cmds.connectAttr(color_constant + ".outColor", spotlight2 + ".color")

# Connect to all RGB as well
for rgb_channel in ["R", "G", "B"]:
    cmds.connectAttr(
        color_constant + f".outColor{rgb_channel}", spotlight1 + f".color{rgb_channel}"
    )
    cmds.connectAttr(
        color_constant + f".outColor{rgb_channel}", spotlight2 + f".color{rgb_channel}"
    )
