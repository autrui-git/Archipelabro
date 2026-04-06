from __future__ import annotations
from typing import TYPE_CHECKING

# Archipelago modules
from BaseClasses import Entrance, Region

# My worlds files
if TYPE_CHECKING:
    from .world import BroforceWorld


def create_and_connect_regions(world: BroforceWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: BroforceWorld) -> None:
    overworld = Region("Overworld", world.player, world.multiworld)
    test_region_1 = Region("Test Region 1", world.player, world.multiworld)

    regions = [overworld, test_region_1]

    # connect regions
    world.multiworld.regions += regions


def connect_regions(world: BroforceWorld) -> None:
    # grab connected regions
    overworld = world.get_region("Overworld")
    test_region_1 = world.get_region("Test Region 1")

    # create an Entrance
    overworld.connect(test_region_1, "Overworld to Test Region 1")