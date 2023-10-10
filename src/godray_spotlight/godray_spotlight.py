import time
from maya import cmds

# Create a slightly warm spotlight
spotlight = cmds.spotLight(coneAngle=40, penumbra=10)
cmds.setAttr(spotlight + ".aiUseColorTemperature", 1)
cmds.setAttr(spotlight + ".aiColorTemperature", 5000)
cmds.setAttr(spotlight + ".aiExposure", 10)

# Disable all rays except volume
cmds.setAttr(spotlight + ".aiDiffuse", 0.0)
cmds.setAttr(spotlight + ".aiSpecular", 0.0)
cmds.setAttr(spotlight + ".aiSss", 0.0)
cmds.setAttr(spotlight + ".aiIndirect", 0.0)

# Get the spotlight's parent transform
spotlight_transform = cmds.listRelatives(spotlight, parent=True)
if spotlight_transform:
    spotlight_transform = spotlight_transform[-1]

# Rotate the light to point downward
cmds.rotate(-90, 0, 0, spotlight_transform)

# Create a noise texture
noise_node = cmds.shadingNode("noise", asTexture=True)
cmds.setAttr(noise_node + ".frequency", 20)

# Connect the noise to the spotlight through a gobo
gobo_node = cmds.shadingNode("aiGobo", asUtility=True)
cmds.connectAttr(gobo_node + ".message", spotlight + ".aiFilters[0]")
cmds.connectAttr(noise_node + ".outColor", gobo_node + ".slidemap")

# Name the spotlight
timestamp = str(int(time.time()))[-5:]
cmds.rename(spotlight_transform, "spot_gobo_noise_" + timestamp)
