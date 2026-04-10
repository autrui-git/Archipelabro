import asyncio
from collections.abc import Sequence

import colorama

from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, CommonContext, server_loop

class ArchipelabroContext(CommonContext):
	game = "Archipelabro"
	items_handling = 0b111 # full remote
	archipelabro_version = "0.0.1"

	def __init__ (self, server_address: str | None = None, password: str | None = None):
		super().__init__(server_address, password)

	async def server_auth (self, password_requested: bool = False) -> None:
		if password_requested and not self.password:
			await self.server_auth(password_requested)
		await self.get_username()
		await self.send_connect(game=self.game)


async def main (args) -> None:
	ctx = ArchipelabroContext(args.connect, args.password)

	ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

	if gui_enabled:
		ctx.run_gui()
	ctx.run_cli()

	await ctx.exit_event.wait()
	await ctx.shutdown()


def launch_archipelabro_client () -> None:
    parser = get_base_parser()
    args = parser.parse_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
