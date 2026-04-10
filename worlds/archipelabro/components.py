from worlds.LauncherComponents import Component, Type, components, launch_subprocess, icon_paths
from Utils import local_path

def run_client() -> None:
	from .client import launch_archipelabro_client
	launch_subprocess(launch_archipelabro_client, name = "Archipelabro Client")


icon_paths['broforce_icon'] = "ap:worlds.archipelabro/assets/broforce_icon.ico"

components.append(
	Component(
		"Archipelabro Client",
		func = run_client,
		game_name = "Archipelabro",
		component_type = Type.CLIENT,
		icon = 'broforce_icon',
	)
)