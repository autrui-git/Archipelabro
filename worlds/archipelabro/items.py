from __future__ import annotations
from typing import TYPE_CHECKING


# Archipelago modules
from BaseClasses import Item, ItemClassification

# My worlds files
if TYPE_CHECKING:
    from .world import BroforceWorld

ITEM_NAME_TO_ID = {
    "Test Item": 1,
    "Filler": 2,
    "Trap": 3,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Test Item": ItemClassification.progression,
    "Filler": ItemClassification.filler,
    "Trap": ItemClassification.trap,
}

class BroforceItem(Item):
    game = "Archipelabro"


def get_random_filler_item_name(world: BroforceWorld) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return "Trap"
    return "Filler"

def create_item_with_correct_classification(world: BroforceWorld, name: str) -> BroforceItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # here : add condition to change item classification (can depend of an option for example)

    return BroforceItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: BroforceWorld) -> None:
    # create regular items
    itempool: list[Item] = [
        world.create_item("Test Item")
    ]

    # create filler items
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool