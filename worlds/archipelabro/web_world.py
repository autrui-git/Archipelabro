# Archipelago modules
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class BroforceWebWorld(WebWorld):
    game = "Archipelabro"

    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Broforce for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["autrui.jpeg"],
    )
    setup_fr = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Broforce for MultiWorld.",
        "French",
        "setup_fr.md",
        "setup/fr",
        ["autrui.jpeg"],
    )

    tutorials = [setup_en, setup_fr]