from collections.abc import Mapping
from typing import Any


# Archipelago modules
from worlds.AutoWorld import World

# My worlds files
from . import web_world, items, locations, regions, rules
from . import options as broforce_options

class BroforceWorld (World):
    """
    Archipelabro is a randomizer for the original Broforce. 
    Broforce is a side-scrolling run and gun game developed by Free Lives and published by Devolver Digital. 
    You play several "bros" (a gender neutral term here), based on action movie icons like John Rambo or Ellen Ripley.
    The goal is to rescue other "bros" in highly destructible environments and defeat the devil boss.
    """

    game = "Archipelabro"

    web = web_world.BroforceWebWorld()
    
    # associate options
    options_dataclass = broforce_options.BroforceOptions
    options: broforce_options.BroforceOptions
    
    apworld_version = 1

    # those need to be static in the world
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # this Override origin_region_name. default: "Menu"
    origin_region_name = "Overworld"

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, create_items.
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.BroforceItem:
        return items.create_item_with_correct_classification(self, name)

    # to get filler items...
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict()