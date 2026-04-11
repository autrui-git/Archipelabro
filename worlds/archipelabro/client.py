import asyncio
from collections.abc import Sequence

import colorama

from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, CommonContext, server_loop

# communication between game and client
import socket
import time
host, port = "127.0.0.1", 25001


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


# Stock usefull data to properly sync with the game
class SyncToBroforce():
	connected_to_broforce = False
	stop_sync = False
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

async def try_disconnect_broforce (stb: SyncToBroforce) -> None:
	print("Try disconnect broforce...")
	try:
		stb.sock.close()
	except Exception as e:
		print(f"executing stb.sock.close() failed: {e}")
	else:
		stb.connected_to_broforce = False
		print("Disconnected broforce")

async def try_connect_broforce (stb: SyncToBroforce) -> None:
	print("Try connect broforce...")
	stb.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		stb.sock.connect((host, port))
	except Exception as e:
		print(f"Connection failed: {e}")
	else:
		stb.connected_to_broforce = True;
		print(f"{time.strftime('%X')} - Connection complete !")

async def send_data(data: str, stb: SyncToBroforce):
	try:
		stb.sock.sendall(data.encode("UTF-8"))
	except Exception as e:
		await try_disconnect_broforce(stb)
		return f"stb.sock.sendall failed : {e}"
	receivedData = ""
	try: 
		receivedData = stb.sock.recv(1024).decode("UTF-8")
	except Exception as e:
		await try_disconnect_broforce(stb)
		return f"stb.sock.recv failed : {e}"
	else:
		return receivedData

async def send_ping_to_broforce (stb: SyncToBroforce) -> None:
	print(f"{time.strftime('%X')} - send PING to broforce")
	receivedData = await send_data("ping", stb)
	if receivedData == "pong":
		print(f"{time.strftime('%X')} - received PONG from broforce")
	else:
		print(f"{time.strftime('%X')} - Wrong data received : {receivedData}")


async def communication_with_broforce (stb: SyncToBroforce) -> None:
	time_since_last_ping = 0
	while not stb.stop_sync:
		if stb.connected_to_broforce:
			await asyncio.sleep(0.5)
			time_since_last_ping += 0.5
			if time_since_last_ping >= 10:
				await send_ping_to_broforce(stb)
				time_since_last_ping = 0
		else:
			await asyncio.sleep(5)
			await try_connect_broforce(stb)

	print(f"finished communication whith game at {time.strftime('%X')}")

async def main (args) -> None:
	print(f"started at {time.strftime('%X')}")
	ctx = ArchipelabroContext(args.connect, args.password)

	ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

	if gui_enabled:
		ctx.run_gui()
	ctx.run_cli()

	stb = SyncToBroforce()
	asyncio.create_task(communication_with_broforce(stb))

	await ctx.exit_event.wait()
	stb.stop_sync = True
	await ctx.shutdown()
	print(f"finished at {time.strftime('%X')}")

def launch_archipelabro_client () -> None:
	parser = get_base_parser()
	args = parser.parse_args()
	colorama.init()
	asyncio.run(main(args))
	colorama.deinit()
