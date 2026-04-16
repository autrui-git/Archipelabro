from dataclasses import dataclass

# Archipelago modules
from Options import DeathLink, PerGameCommonOptions, Range

class TrapChance(Range):

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0

@dataclass
class BroforceOptions (PerGameCommonOptions):
    death_link: DeathLink
    trap_chance: TrapChance
