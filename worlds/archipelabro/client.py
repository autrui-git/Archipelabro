import asyncio
# -------------- Section start : Communication between Broforce and this client -----------------------------------
import socket
import time

import colorama

import Utils
from CommonClient import gui_enabled, get_base_parser, CommonContext, server_loop

# from .syncToBroforce import SyncToBroforce, communication_with_broforce
host, port = "127.0.0.1", 25001

# Stock usefull data to properly sync with the game
def is_a_request (request: str):
	return request in ["send_DeathLink"]


class SyncToBroforce:
	#sync_task: typing.Optional["asyncio.Task[None]"] = None
	connected_to_broforce = False
	stop_sync = False
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	send_request_buffer = []
	received_request_buffer = []
	requests_responses = {
		"do_DeathLink": "DeathLink_noted",
	}
	deathlink_pending = False

	async def try_disconnect_broforce (self) -> None:
		# print("Try disconnect broforce...")
		try:
			self.sock.close()
		except Exception as e:
			print(f"executing sock.close() failed: {e}")
		else:
			self.connected_to_broforce = False
			print("Disconnected broforce")

	async def try_connect_broforce (self) -> None:
		# print("Try connect broforce...")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.sock.connect((host, port))
		except:
			#print(f"Connection failed: {e}")
			pass
		else:
			self.connected_to_broforce = True
			print(f"{time.strftime('%X')} - Connection to Broforce complete !")

	async def send_data(self, data: str):
		print(f"send : {data} to Broforce")
		try:
			self.sock.sendall(data.encode("UTF-8"))
		except Exception as e:
			await self.try_disconnect_broforce()
			print(f"sock.recv failed : {e}")
			return "Error"
		try: 
			received_data = self.sock.recv(1024).decode("UTF-8")
		except Exception as e:
			await self.try_disconnect_broforce()
			print(f"sock.recv failed : {e}")
			return "Error"
		else:
			print(f"received : {received_data} from Broforce")
			return received_data


# -------------- Section end : Communication between Broforce and this client -------------------------------------




class ArchipelabroContext(CommonContext):
	game = "Archipelabro"
	items_handling = 0b111 # full remote
	archipelabro_version = "0.0.1"

	is_connected : bool
	deathlink_enabled : bool
	deathlink_pending : bool

	stb: SyncToBroforce

	def __init__ (self, server_address: str | None = None, password: str | None = None):
		super().__init__(server_address, password)
		
		self.broforce_slot_data = None

		self.is_connected = False
		self.deathlink_enabled = False
		self.deathlink_pending = False

	async def server_auth (self, password_requested: bool = False) -> None:
		if password_requested and not self.password:
			await self.server_auth(password_requested)
		await self.get_username()
		await self.send_connect(game=self.game)

	async def shutdown(self, stb: SyncToBroforce | None = None):
		if stb is not None:
			stb.stop_sync = True
			while stb.connected_to_broforce:
				pass
		await super(ArchipelabroContext, self).shutdown()

	# -------------------- Package management --------------------
	def on_package(self, cmd: str, args: dict) -> None:
		if cmd == "Connected":
			self.broforce_slot_data = args["slot_data"]
			if "death_link" in self.broforce_slot_data and self.broforce_slot_data["death_link"]:
				Utils.async_start(self.update_death_link(True))
				self.deathlink_enabled = True
			self.is_connected = True

		if cmd == "Bounced":
			if "tags" in args:
				if "DeathLink" in args["tags"]:
					self.on_deathlink(args["data"])

	def on_deathlink(self, data: dict) -> None:
		if self.deathlink_pending:
			return
		self.deathlink_pending = True
		self.stb.send_request_buffer.append("do_DeathLink")
		super().on_deathlink(data)
		Utils.async_start(self.wait_and_lower_deathlink_flag())

	def send_death(self, death_text: str = "") -> None:
		# What should be done to send a death link
		# Avoid sending death if we died from a deathlink
		if self.deathlink_pending or not self.deathlink_enabled:
			return
		self.deathlink_pending = True
		Utils.async_start(super().send_death(death_text))
		Utils.async_start(self.wait_and_lower_deathlink_flag())

	async def wait_and_lower_deathlink_flag(self) -> None:
		await asyncio.sleep(3)
		self.deathlink_pending = False

async def wait_alone () -> None:
	while True:
		pass

async def communication_with_broforce (stb: SyncToBroforce, ctx: ArchipelabroContext) -> None:
	while not stb.stop_sync:
		await asyncio.sleep(0.5)
		if stb.connected_to_broforce:
			if len(stb.send_request_buffer) > 0:
				request = stb.send_request_buffer[0]
				response = await stb.send_data(request)
				if response == stb.requests_responses[request]: # if the game well received the request
					stb.send_request_buffer.remove(request)
					print(f"Send {request} to game.")
			else:
				request = await stb.send_data("ask")
				if is_a_request(request):
					match request:
						case "send_DeathLink":
							ctx.send_death("bro died")
					print(f"Receive {request} from game.")
		else:
			await asyncio.sleep(5)
			await stb.try_connect_broforce()
	await stb.try_disconnect_broforce
	stb.connected_to_broforce = False


async def main (args) -> None:
	print(f"started at {time.strftime('%X')}")

	stb = SyncToBroforce()

	ctx = ArchipelabroContext(args.connect, args.password)
	ctx.stb = stb

	
	asyncio.create_task(communication_with_broforce(stb, ctx), name="sync with game loop")

	ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")


	if gui_enabled:
		ctx.run_gui()
	ctx.run_cli()

	await ctx.exit_event.wait()
	await ctx.shutdown(stb)
	print(f"finished at {time.strftime('%X')}")

def launch_archipelabro_client () -> None:
	parser = get_base_parser()
	args = parser.parse_args()
	colorama.init()
	asyncio.run(main(args))
	colorama.deinit()
