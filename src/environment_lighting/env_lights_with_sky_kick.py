import maya.cmds as cmds
from math import sqrt

# NOTE
# Environment light exposure is based on that light's distance,
# which is based on the character lights distances (namely the key light.)
# Assumption is that character light exposure is based on distance as well.
# Environment light colors are based on character light colors.
# If character is lit by color temperature, env light temp is easier
# If character is lit by color w/o temp, find appropriate colors based on these
#   e.g. if character is in purple, maybe scene is sunset, so we use desaturated purple for sky
#       simple rule, just desaturate given color?
#       rule for temps, just move slightly further (or closer?) from white?

CHARACTER_RIG_NAME = "characterRig"
ENV_LIGHT_RIG_NAME = "environmentRig"
SUN_GROUP_NAME = "sunLights"

SUN_BEAM = "sun_beam"
SUN_SPILL = "sun_spill"
SKY_DIFFUSE = "sky_diffuse"
SKY_KICK = "sky_kick"

DISABLED_SKY_RAYS = ["aiSpecular", "aiSss", "aiIndirect", "aiVolume"]
SKY_BOUNCES = 0

SUN_DISTANCE_MULTIPLIER = 10

character_light_group = None
spot_lights = {}
area_lights = {}
spot_light_transforms = {}
area_light_transforms = {}


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


# Find the character rig
def get_character_rig(name: str):
    character_light_group_exists = cmds.objExists(name)
    if character_light_group_exists is True:
        character_light_group = cmds.ls(name)[0]
    else:
        # Logging this error ends script execution
        cmds.error("Character lights not found.\n" f"expected group with name: {name}")

    return character_light_group


# Create all the environment lights
create_spot_light(SUN_BEAM, spot_lights, spot_light_transforms)
create_spot_light(SUN_SPILL, spot_lights, spot_light_transforms)
create_area_light(SKY_DIFFUSE, area_lights, area_light_transforms)
create_area_light(SKY_KICK, area_lights, area_light_transforms)

# Get character lighting details
character_light_group = get_character_rig(name=CHARACTER_RIG_NAME)
# Position
character_key = {"transform": None, "light": None, "ws_position": None}
character_key["transform"] = cmds.ls("character_key")[0]
character_key_children = cmds.listRelatives(character_key["transform"], children=True)
character_key["light"] = character_key_children[0]
character_key["ws_position"] = cmds.xform(character_key["transform"], q=1, ws=1, rp=1)

character = cmds.ls("mainCharacter")[0]
character_ws_position = cmds.xform(character, q=1, ws=1, rp=1)
character_to_key_distance = euclidean_distance(
    character_ws_position, character_key["ws_position"]
)

# Get character lights colors
# Get key light color and whether it uses temp

# Adjust environment lights
# Position
# Set Sun light positions based on character key light
sun_group = cmds.group(em=True, name=SUN_GROUP_NAME)
cmds.parent(spot_light_transforms[SUN_BEAM], sun_group)
cmds.parent(spot_light_transforms[SUN_SPILL], sun_group)
sun_y_distance = character_to_key_distance * SUN_DISTANCE_MULTIPLIER
set_attr(sun_group, "translateY", sun_y_distance)
set_attr(sun_group, "rotateX", -90)

# Set Sky Diffuse pointing down from above character
sky_diffuse_distance = sun_y_distance / 5
set_attr(area_light_transforms[SKY_DIFFUSE], "translateY", sky_diffuse_distance)
set_attr(area_light_transforms[SKY_DIFFUSE], "rotateX", -90)

# Set Sky Kick position (opposite character key, same distance as sky diffuse)
sky_kick_distance = sky_diffuse_distance
# set_attr(area_light_transforms[SKY_DIFFUSE], "translateY", sky_diffuse_distance)


# Exposure and Color
# Sun Exposure
sun_beam_exposure = sun_y_distance / 6.75
sun_spill_exposure = sun_beam_exposure * 0.9
set_attr(spot_light_transforms[SUN_BEAM], "aiExposure", sun_beam_exposure)
set_attr(spot_light_transforms[SUN_SPILL], "aiExposure", sun_spill_exposure)

# Sky Exposure
sky_diffuse_exposure = sun_y_distance / 15
sky_kick_exposure = sky_diffuse_exposure / 2
set_attr(area_lights[SKY_DIFFUSE], "aiExposure", sky_diffuse_exposure)
set_attr(area_lights[SKY_KICK], "aiExposure", sky_kick_exposure)

# Sky Area Scales
sky_diffuse_scale = sun_y_distance / 5
sky_kick_scale = sky_diffuse_scale * 0.75
set_attr(area_light_transforms[SKY_DIFFUSE], "scaleX", sky_diffuse_scale)
set_attr(area_light_transforms[SKY_DIFFUSE], "scaleY", sky_diffuse_scale)
set_attr(area_light_transforms[SKY_DIFFUSE], "scaleZ", sky_diffuse_scale)
set_attr(area_light_transforms[SKY_KICK], "scaleX", sky_kick_scale)
set_attr(area_light_transforms[SKY_KICK], "scaleY", sky_kick_scale)
set_attr(area_light_transforms[SKY_KICK], "scaleZ", sky_kick_scale)


# Environment light colors are based on character light colors.
# If character is lit by color temperature, env light temp is easier
# If character is lit by color w/o temp, find appropriate colors based on these
#   e.g. if character is in purple, maybe scene is sunset, so we use desaturated purple for sky
#       simple rule, just desaturate given color?
#       rule for temps, just move slightly further (or closer?) from white?

# Sun Color
sun_beam_temp = 6000
sun_spill_temp = 5200
set_attr(spot_lights[SUN_BEAM], "aiUseColorTemperature", 1)
set_attr(spot_lights[SUN_SPILL], "aiUseColorTemperature", 1)
set_attr(spot_lights[SUN_BEAM], "aiColorTemperature", sun_beam_temp)
set_attr(spot_lights[SUN_SPILL], "aiColorTemperature", sun_spill_temp)

# Sky Color
sky_diffuse_temp = 9000
sky_kick_temp = 9000
set_attr(area_lights[SKY_DIFFUSE], "aiUseColorTemperature", 1)
set_attr(area_lights[SKY_KICK], "aiUseColorTemperature", 1)
set_attr(area_lights[SKY_DIFFUSE], "aiColorTemperature", sky_diffuse_temp)
set_attr(area_lights[SKY_KICK], "aiColorTemperature", sky_kick_temp)

# Sun Beam + Spill radius
sun_beam_radius = sun_y_distance / 40
sun_spill_radius = sun_y_distance / 7.5
set_attr(spot_light_transforms[SUN_BEAM], "aiRadius", sun_beam_radius)
set_attr(spot_light_transforms[SUN_SPILL], "aiRadius", sun_spill_radius)

# Ray Types
# Remove specular from Sky diffuse and kick
for ray_type in DISABLED_SKY_RAYS:
    set_attr(area_lights[SKY_DIFFUSE], ray_type, 0)
    set_attr(area_lights[SKY_KICK], ray_type, 0)

set_attr(area_lights[SKY_DIFFUSE], "aiMaxBounces", SKY_BOUNCES)
set_attr(area_lights[SKY_KICK], "aiMaxBounces", SKY_BOUNCES)

# Group the environment lights
env_light_group = cmds.group(em=True, name=ENV_LIGHT_RIG_NAME)
cmds.parent(sun_group, env_light_group)

for area_light_transform in area_light_transforms.values():
    cmds.parent(area_light_transform, env_light_group)

cmds.parent(character_light_group, env_light_group)
