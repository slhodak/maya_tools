from maya import cmds

from ..paths import DEFAULT_ICON
from .light_rig.easy_light_rig import create_easy_light_rig
from .light_pair.spotlight_pair import create_spotlight_pair
from .environment_lighting.environment_lighting import (
    set_up_environment_lighting_around_character,
)

CUSTOM_SHELF_NAME = "SScripts"


def add_environment_lighting_button(shelf):
    print("Creating easy light rig button")
    cmds.shelfButton(
        parent=shelf,
        i=DEFAULT_ICON,
        c=set_up_environment_lighting_around_character,
        label="EnvLights",
        annotation="Create environment lights based on existing character lighting",
    )


def add_easy_light_rig_button(shelf):
    print("Creating easy light rig button")
    cmds.shelfButton(
        parent=shelf,
        i=DEFAULT_ICON,
        c=create_easy_light_rig,
        label="LightPair",
        annotation="Create simple 3-point lighting rig with a camera",
    )


def add_spotlight_pair_button(shelf):
    print("Creating spotlight pair button")
    cmds.shelfButton(
        parent=shelf,
        i=DEFAULT_ICON,
        c=create_spotlight_pair,
        label="LightPair",
        annotation="Create two linked spot lights",
    )


# Search the layout tree until you get to the tool shelves
def find_main_shelf_layout(node: str):
    if "button" in node.lower():
        return None

    children = cmds.layout(node, q=1, childArray=1)
    # Confirm we found the main shelf layout
    # And will return the node even if it is found on the first call
    if "Animation" in children:
        return node

    for child in children:
        node_found = find_main_shelf_layout(f"{node}|{child}")
        if node_found is not None:
            return node_found

    return None


def add_or_update_custom_shelf():
    print("Running SScripts Shelf Setup")
    main_shelf = find_main_shelf_layout("Shelf")
    children = cmds.layout(main_shelf, q=1, childArray=1)
    if CUSTOM_SHELF_NAME in children:
        cmds.deleteUI(f"{main_shelf}|{CUSTOM_SHELF_NAME}")

    custom_shelf = cmds.shelfLayout(CUSTOM_SHELF_NAME, parent=main_shelf)
    add_easy_light_rig_button(custom_shelf)
    add_spotlight_pair_button(custom_shelf)
    add_environment_lighting_button(custom_shelf)
