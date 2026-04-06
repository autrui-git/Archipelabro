from __future__ import annotations
from typing import TYPE_CHECKING

# Archipelago modules
from BaseClasses import ItemClassification, Location

# My worlds files
from . import items

if TYPE_CHECKING:
    from .world import BroforceWorld


LOCATION_NAME_TO_ID = {
    "Location Test 1": 1,
    "Location Test 2": 2,
}

class BroforceLocation(Location):
    game="Archipelabro"

    
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}



def create_all_locations(world: BroforceWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: BroforceWorld) -> None:
    # grab connected regions
    overworld = world.get_region("Overworld")
    test_region_1 = world.get_region("Test Region 1")

    # add locations
    test_region_1_locations = get_location_names_with_ids(
        ["Location Test 1", "Location Test 2"]
    )
    test_region_1.add_locations(test_region_1_locations, BroforceLocation)

# events are locations that are part of logic but not in the randomizer. so they are not in LOCATION_NAME_TO_ID
def create_events(world: BroforceWorld) -> None:
    # grab connected regions
    overworld = world.get_region("Overworld")
    test_region_1 = world.get_region("Test Region 1")

    # add events
    overworld.addevent(
        "Try event", "It's a try", location_type=BroforceLocation, item_type=items.BroforceItem
    )
    test_region_1.addevent(
        "Winning condition", "Victory", location_type=BroforceLocation, item_type=items.BroforceItem
    )