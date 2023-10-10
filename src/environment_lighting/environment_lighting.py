import maya.cmds as cmds
from math import sqrt

CHARACTER_NAME = "mainCharacter"
CHARACTER_RIG_NAME = "characterLightRig"
CHARACTER_KEY_NAME = "onCharacter_key"
ENV_LIGHT_RIG_NAME = "environmentRig"
SUN_GROUP_NAME = "sunLights"

SUN_BEAM = "sun_beam"
SUN_SPILL = "sun_spill"
SKY_DIFFUSE = "sky_diffuse"

DISABLED_SKY_RAYS = ["aiSpecular", "aiSss", "aiIndirect", "aiVolume"]
SKY_BOUNCES = 0

SUN_DISTANCE_RATIO = 10  # sun distance = key distance * this value
SUN_BEAM_RADIUS_RATIO = 0.025  # beam radius = sun dist * this value
SUN_SPILL_RADIUS_RATIO = 0.13  # spill radius = sun dist * this value
SUN_SPILL_EXPOSURE_RATIO = 0.85  # spill exposure = beam exposure * this value
SKY_DIFFUSE_EXPOSURE_RATIO = 0.75  # sky exposure = sun exposure * this value
SKY_DIFFUSE_DISTANCE_RATIO = 0.20  # sky distance = sun dist * this value
SKY_DIFFUSE_SCALE_RATIO = 1.0  # sky scale = sky dist * this value

SUN_BEAM_TEMP_DEFAULT = 6000
SUN_SPILL_TEMP_RATIO = 0.85  # spill temp = beam temp * this value
SKY_DIFFUSE_TEMP_RATIO = 1.45  # sky temp = beam temp * this value

character_light_group = None
spot_lights = {}
area_lights = {}
spot_light_transforms = {}
area_light_transforms = {}

######################
### Helper Methods ###
######################


# Maya light creation returns the light itself
# Add to lights and transforms
def create_spot_light(light_name: str, lights: dict, transforms: dict):
    spot_light = cmds.spotLight(name=f"{light_name}_spot")
    lights[light_name] = spot_light
    # Get the transform
    sun_beam_transform = cmds.listRelatives(spot_light, parent=True)
    if sun_beam_transform:
        sun_beam_transform = sun_beam_transform[0]
        transforms[light_name] = sun_beam_transform
    else:
        cmds.error("Could not get transform for spot light")


# Arnold light creation returns the transform
# Add to lights and transforms
def create_area_light(light_name: str, lights: dict, transforms: dict):
    area_light_transform = cmds.shadingNode(
        "aiAreaLight", asLight=True, name=f"{light_name}_areaShape"
    )
    transforms[light_name] = area_light_transform
    area_light = cmds.listRelatives(area_light_transform, children=True)
    # Get the lightShape
    if area_light:
        area_light = area_light[0]
        lights[light_name] = area_light
    else:
        cmds.error("Could not get light object for area light")


def set_attr(obj_name: str, attribute: str, value: any):
    cmds.setAttr(f"{obj_name}.{attribute}", value)


def euclidean_distance(a: list, b: list):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def calculate_sun_exposure(sun_distance: float):
    return 43.71969 + (-3.606164 - 43.71969) / (
        1 + (sun_distance / 748.8465) ** 0.2575185
    )


def calculate_sky_exposure(sky_distance: float):
    return 43.71969 + (-3.606164 - 43.71969) / (
        1 + (sky_distance / 748.8465) ** 0.2575185
    )


# Find the character rig
def get_character_rig(name: str):
    character_light_group_exists = cmds.objExists(name)
    if character_light_group_exists is True:
        character_light_group = cmds.ls(name)[0]
    else:
        # Logging this error ends script execution
        cmds.error("Character lights not found.\n" f"expected group with name: {name}")

    return character_light_group


def set_up_environment_lighting_around_character():
    # Create all the environment lights
    create_spot_light(SUN_BEAM, spot_lights, spot_light_transforms)
    create_spot_light(SUN_SPILL, spot_lights, spot_light_transforms)
    create_area_light(SKY_DIFFUSE, area_lights, area_light_transforms)

    ###################################
    ### Get Character Lighting Data ###
    ###################################

    character_light_group = get_character_rig(name=CHARACTER_RIG_NAME)

    ### Position
    character_key = {"transform": None, "light": None, "ws_position": None}
    character_key["transform"] = cmds.ls(CHARACTER_KEY_NAME)[0]
    if character_key["transform"] is None:
        cmds.error(
            f"Could not find character key light, expected name: {CHARACTER_KEY_NAME}"
        )

    character_key_children = cmds.listRelatives(character_key["transform"], children=True)
    character_key["light"] = character_key_children[0]
    character_key["ws_position"] = cmds.xform(character_key["transform"], q=1, ws=1, rp=1)

    character = cmds.ls(CHARACTER_NAME)[0]
    if character is None:
        cmds.error(
            f"Could not find main character, expected name: {CHARACTER_NAME}"
        )

    character_ws_position = cmds.xform(character, q=1, ws=1, rp=1)
    character_to_key_distance = euclidean_distance(
        character_ws_position, character_key["ws_position"]
    )

    ### Color
    character_key["uses_color_temp"] = (
        cmds.getAttr(f"{character_key['light']}.aiUseColorTemperature") == 1
    )
    if character_key["uses_color_temp"] is True:
        character_key["color_temp"] = cmds.getAttr(
            f"{character_key['light']}.aiColorTemperature"
        )
    else:
        character_key["color"] = cmds.getAttr(f"{character_key['light']}.color")

    #################################
    ### Adjust Environment Lights ###
    #################################

    ### Position
    # Set Sun light positions based on character key light
    sun_group = cmds.group(em=True, name=SUN_GROUP_NAME)
    cmds.parent(spot_light_transforms[SUN_BEAM], sun_group)
    cmds.parent(spot_light_transforms[SUN_SPILL], sun_group)
    sun_y_distance = character_to_key_distance * SUN_DISTANCE_RATIO
    set_attr(sun_group, "translateY", sun_y_distance)
    set_attr(sun_group, "rotateX", -90)

    # Set Sky Diffuse pointing down from above character
    sky_diffuse_distance = sun_y_distance * SKY_DIFFUSE_DISTANCE_RATIO
    set_attr(area_light_transforms[SKY_DIFFUSE], "translateY", sky_diffuse_distance)
    set_attr(area_light_transforms[SKY_DIFFUSE], "rotateX", -90)

    # Sky area scale
    sky_diffuse_scale = sky_diffuse_distance * SKY_DIFFUSE_SCALE_RATIO
    set_attr(area_light_transforms[SKY_DIFFUSE], "scaleX", sky_diffuse_scale)
    set_attr(area_light_transforms[SKY_DIFFUSE], "scaleY", sky_diffuse_scale)
    set_attr(area_light_transforms[SKY_DIFFUSE], "scaleZ", sky_diffuse_scale)

    ### Exposure
    # Sun Exposure
    sun_beam_exposure = calculate_sun_exposure(sun_y_distance)
    sun_spill_exposure = sun_beam_exposure * SUN_SPILL_EXPOSURE_RATIO
    set_attr(spot_light_transforms[SUN_BEAM], "aiExposure", sun_beam_exposure)
    set_attr(spot_light_transforms[SUN_SPILL], "aiExposure", sun_spill_exposure)

    # Sky Exposure
    sky_diffuse_exposure = sun_beam_exposure * SKY_DIFFUSE_EXPOSURE_RATIO
    set_attr(area_lights[SKY_DIFFUSE], "aiExposure", sky_diffuse_exposure)

    ### Color
    # Environment light colors are based on character light colors.
    # If character is lit by color temperature, env light temp is easier
    # TODO: If character is lit by color w/o temp, find appropriate colors based on these

    sun_beam_temp = SUN_BEAM_TEMP_DEFAULT

    if character_key["uses_color_temp"] is True:
        sun_beam_temp = character_key["color_temp"]

    sun_spill_temp = sun_beam_temp * SUN_SPILL_TEMP_RATIO
    sky_diffuse_temp = sun_beam_temp * SKY_DIFFUSE_TEMP_RATIO

    # Sun Color
    set_attr(spot_lights[SUN_BEAM], "aiUseColorTemperature", 1)
    set_attr(spot_lights[SUN_SPILL], "aiUseColorTemperature", 1)
    set_attr(spot_lights[SUN_BEAM], "aiColorTemperature", sun_beam_temp)
    set_attr(spot_lights[SUN_SPILL], "aiColorTemperature", sun_spill_temp)

    # Sky Color
    set_attr(area_lights[SKY_DIFFUSE], "aiUseColorTemperature", 1)
    set_attr(area_lights[SKY_DIFFUSE], "aiColorTemperature", sky_diffuse_temp)

    # Sun Beam + Spill radius
    sun_beam_radius = sun_y_distance * SUN_BEAM_RADIUS_RATIO
    sun_spill_radius = sun_y_distance * SUN_SPILL_RADIUS_RATIO
    set_attr(spot_light_transforms[SUN_BEAM], "aiRadius", sun_beam_radius)
    set_attr(spot_light_transforms[SUN_SPILL], "aiRadius", sun_spill_radius)

    # Ray Types
    # Remove specular from Sky diffuse
    for ray_type in DISABLED_SKY_RAYS:
        set_attr(area_lights[SKY_DIFFUSE], ray_type, 0)

    set_attr(area_lights[SKY_DIFFUSE], "aiMaxBounces", SKY_BOUNCES)

    # Group the environment lights
    env_light_group = cmds.group(em=True, name=ENV_LIGHT_RIG_NAME)
    cmds.parent(sun_group, env_light_group)

    for area_light_transform in area_light_transforms.values():
        cmds.parent(area_light_transform, env_light_group)

    cmds.parent(character_light_group, env_light_group)
