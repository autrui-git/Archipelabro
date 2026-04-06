from __future__ import annotations
from typing import TYPE_CHECKING


# Archipelago modules
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule


# My worlds files
if TYPE_CHECKING:
    from .world import BroforceWorld


def set_all_rules(world: BroforceWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: BroforceWorld) -> None:
    # grab connected entrances
    overworld_to_test_region_1 = world.get_entrance("Overworld to Test Region 1")

    # add rules
    set_rule(overworld_to_test_region_1, lambda state: state.has("It's a try", world.player))

def set_all_location_rules(world: BroforceWorld) -> None:
    # grab connected locations
    location_test_2 = world.get_location("Location Test 2")

    # add rules
    set_rule(location_test_2, lambda state: state.has("Test Item", world.player))

def set_completion_condition(world: BroforceWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)