import maya.cmds as cmds

DIALOG_NAME = "init_texture_shader_dialog"


def init_texture_shader_dialog():
    if cmds.window(DIALOG_NAME, exists=True):
        cmds.deleteUI(DIALOG_NAME)

    dialog = cmds.window(DIALOG_NAME, title="Initialize Texture Shader")

    cmds.columnLayout(adjustableColumn=True, height=150)
    albedo_checkbox = cmds.checkBox("Albedo Map", value=True)
    roughness_checkbox = cmds.checkBox("Roughness Map", value=True)
    normal_checkbox = cmds.checkBox("Normal Map", value=True)
    metallic_checkbox = cmds.checkBox("Metallic Map", value=False)
    ao_checkbox = cmds.checkBox("Ambient Occlusion (Map)", value=False)

    # command always passes one boolean argument
    def call_init_texture_shader(x):
        init_texture_shader(
            albedo_checkbox=albedo_checkbox,
            roughness_checkbox=roughness_checkbox,
            normal_checkbox=normal_checkbox,
            metallic_checkbox=metallic_checkbox,
            ao_checkbox=ao_checkbox,
        )

    cmds.button(label="Initialize", command=call_init_texture_shader)
    cmds.showWindow(dialog)


def init_texture_shader(
    albedo_checkbox, roughness_checkbox, normal_checkbox, metallic_checkbox, ao_checkbox
):
    # Shader
    shader_node = cmds.shadingNode(
        "aiStandardSurface", asShader=True, isColorManaged=True
    )
    shadingGroupNode = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(shader_node + ".outColor", shadingGroupNode + ".surfaceShader")

    # Place Texture UV Node
    place_texture_node = cmds.shadingNode("place2dTexture", asUtility=True)

    # Albedo
    if cmds.checkBox(albedo_checkbox, q=1, v=1) is True:
        albedo_file_node = cmds.shadingNode("file", asTexture=True, isColorManaged=True)
        cmds.connectAttr(place_texture_node + ".outUV", albedo_file_node + ".uv")

        # Ambient Occlusion
        # NOTE: Don't (yet? ever?) allow AO input without albedo
        if cmds.checkBox(ao_checkbox, q=1, v=1) is True:
            add_ao_map(place_texture_node, albedo_file_node, shader_node)

        else:
            cmds.connectAttr(albedo_file_node + ".outColor", shader_node + ".baseColor")

    # Roughness
    if cmds.checkBox(roughness_checkbox, q=1, v=1) is True:
        add_roughness_map(place_texture_node, shader_node)

    # Normal
    if cmds.checkBox(normal_checkbox, q=1, v=1) is True:
        add_normal_map(place_texture_node, shader_node)

    # Metallic
    if cmds.checkBox(metallic_checkbox, q=1, v=1) is True:
        add_metallic_map(place_texture_node, shader_node)

    cmds.deleteUI(DIALOG_NAME)


def add_normal_map(place_texture_node, shader_node):
    aiImageNode = cmds.shadingNode("aiImage", asTexture=True, isColorManaged=True)
    aiNormalNode = cmds.shadingNode("aiNormalMap", asShader=True)
    cmds.connectAttr(aiImageNode + ".outColor", aiNormalNode + ".input")
    cmds.connectAttr(aiNormalNode + ".outValue", shader_node + ".normalCamera")
    cmds.connectAttr(place_texture_node + ".outUV", aiImageNode + ".uvcoords")


def add_roughness_map(place_texture_node, shader_node):
    roughness_file_node = cmds.shadingNode("file", asTexture=True, isColorManaged=True)
    roughness_color_to_float_node = cmds.shadingNode("aiColorToFloat", asUtility=True)
    roughness_remap_value_node = cmds.shadingNode("remapValue", asUtility=True)
    cmds.connectAttr(
        roughness_file_node + ".outColor", roughness_color_to_float_node + ".input"
    )
    cmds.connectAttr(
        roughness_remap_value_node + ".outValue",
        shader_node + ".specularRoughness",
    )
    cmds.connectAttr(
        roughness_color_to_float_node + ".outValue",
        roughness_remap_value_node + ".inputValue",
    )
    cmds.connectAttr(place_texture_node + ".outUV", roughness_file_node + ".uv")


def add_metallic_map(place_texture_node, shader_node):
    metallic_file_node = cmds.shadingNode("file", asTexture=True, isColorManaged=True)
    metallic_color_to_float_node = cmds.shadingNode("aiColorToFloat", asUtility=True)
    metallic_remap_value_node = cmds.shadingNode("remapValue", asUtility=True)
    cmds.connectAttr(
        metallic_file_node + ".outColor", metallic_color_to_float_node + ".input"
    )
    cmds.connectAttr(
        metallic_remap_value_node + ".outValue",
        shader_node + ".metalness",
    )
    cmds.connectAttr(
        metallic_color_to_float_node + ".outValue",
        metallic_remap_value_node + ".inputValue",
    )
    cmds.connectAttr(place_texture_node + ".outUV", metallic_file_node + ".uv")


def add_ao_map(place_texture_node, albedo_file_node, shader_node):
    ao_file_node = cmds.shadingNode("file", asTexture=True, isColorManaged=True)
    cmds.connectAttr(place_texture_node + ".outUV", ao_file_node + ".uv")

    ao_math_node = cmds.shadingNode("colorMath", asUtility=True)
    cmds.setAttr(ao_math_node + ".operation", 3)
    cmds.connectAttr(ao_file_node + ".outColor", ao_math_node + ".colorB")

    # Multiply Albedo by AO
    cmds.connectAttr(albedo_file_node + ".outColor", ao_math_node + ".colorA")
    cmds.connectAttr(ao_math_node + ".outColor", shader_node + ".baseColor")
