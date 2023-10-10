import maya.cmds as cmds


def init_texture_shader():
    # Shader
    aiStandardSurfaceNode = cmds.shadingNode(
        "aiStandardSurface", asShader=True, isColorManaged=True
    )
    shadingGroupNode = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(
        aiStandardSurfaceNode + ".outColor", shadingGroupNode + ".surfaceShader"
    )

    # Albedo
    albedoFileNode = cmds.shadingNode("file", asTexture=True, isColorManaged=True)

    # Ambient Occlusion
    # Labeled so you can see what the node is for (b/c it will not be connected by default)
    # Name includes current time so it won't conflict when you run the script again
    aoFileNodeName = "ao_temp_" + cmds.date(format="hhmmss")
    aoFileNode = cmds.shadingNode(
        "file", asTexture=True, isColorManaged=True, name=aoFileNodeName
    )

    # Multiply Albedo by AO
    # By default, color B will be white and file will not be connected,
    # so if there is no AO file, this will have no effect
    aoColorCompositeNode = cmds.shadingNode("colorComposite", asUtility=True)
    cmds.setAttr(aoColorCompositeNode + ".operation", 3)
    cmds.setAttr(aoColorCompositeNode + ".colorB", 1.0, 1.0, 1.0)
    # Label Color Composite node by its intended purpose
    aoColorCompositeNodeNewName = aoColorCompositeNode + "_multiply_AO"
    cmds.rename(aoColorCompositeNode, aoColorCompositeNodeNewName)
    # Name serves as a handle for the object itself - so replace the old reference with the new name
    aoColorCompositeNode = aoColorCompositeNodeNewName
    cmds.connectAttr(albedoFileNode + ".outColor", aoColorCompositeNode + ".colorA")
    cmds.connectAttr(
        aoColorCompositeNode + ".outColor", aiStandardSurfaceNode + ".baseColor"
    )

    # Roughness
    roughnessFileNode = cmds.shadingNode("file", asTexture=True, isColorManaged=True)
    roughnessColorToFloatNode = cmds.shadingNode("aiColorToFloat", asUtility=True)
    roughnessRemapValueNode = cmds.shadingNode("remapValue", asUtility=True)
    cmds.connectAttr(
        roughnessFileNode + ".outColor", roughnessColorToFloatNode + ".input"
    )
    cmds.connectAttr(
        roughnessRemapValueNode + ".outValue",
        aiStandardSurfaceNode + ".specularRoughness",
    )
    cmds.connectAttr(
        roughnessColorToFloatNode + ".outValue", roughnessRemapValueNode + ".inputValue"
    )

    # Normal
    aiImageNode = cmds.shadingNode("aiImage", asTexture=True, isColorManaged=True)
    aiNormalNode = cmds.shadingNode("aiNormalMap", asShader=True)
    cmds.connectAttr(aiImageNode + ".outColor", aiNormalNode + ".input")
    cmds.connectAttr(
        aiNormalNode + ".outValue", aiStandardSurfaceNode + ".normalCamera"
    )

    # UV
    placeTextureNode = cmds.shadingNode("place2dTexture", asUtility=True)
    cmds.connectAttr(placeTextureNode + ".outUV", albedoFileNode + ".uv")
    cmds.connectAttr(placeTextureNode + ".outUV", roughnessFileNode + ".uv")
    cmds.connectAttr(placeTextureNode + ".outUV", aoFileNode + ".uv")
    cmds.connectAttr(placeTextureNode + ".outUV", aiImageNode + ".uvcoords")
