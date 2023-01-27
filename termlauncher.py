import os
from textual.app import App, ComposeResult
from textual.widgets import Header, ListView, ListItem, Label, Footer, DataTable, Input, Static
from textual import log, events
from rich.progress import Progress, BarColumn
import asyncio
#import subprocess
import json
import pyautogui

class mode(Static):

	title = "TermLauncher"

	def on_mount(self) -> None:
		self.reset()

	def reset(self) -> None:
		self.update('TermLauncher')

	def on_click(self) -> None:
		self.next_word()

	def set_content(self, content) -> None:
		"""Get a new hello and update the content area."""
		self.update(f"{content}, [b](l)auncher[/b]")

class IndeterminateProgress(Static):
	def __init__(self):
		super().__init__("")
		self._bar = Progress(BarColumn(250))
		self._bar.add_task("", total=None)

	def on_mount(self) -> None:
		# When the widget is mounted start updating the display regularly.
		self.update_render = self.set_interval(
			1 / 60, self.update_progress_bar
		)

	def update_progress_bar(self) -> None:
		self.update(self._bar)

class KeyLauncher(App):
	"""A Textual key launcher app."""
	CSS_PATH = "keylaunch.css"

	plugins = []
	current_object = {}
	current_plugin = {}
	task = None

	BINDINGS = [
		("d", "toggle_dark", "Toggle dark mode"),
		("esc", "quit", "Quit the app"),
	]

	def on_mount(self) -> None:
		"""Called when the app is mounted."""
		self.query_one(IndeterminateProgress).visible = False
		log("mounted")
		script_directory = os.path.dirname(os.path.realpath(__file__))

		f =open(script_directory + '\settings.json', "r")
		self.settings = json.load(f)
		self.dark = self.settings['darktheme']

		self.plugins = self.settings['plugins']
		f.close()
		#log(self.plugins)
		self.query_one(DataTable).add_columns("keyword", "Plugin", "Description")
		for plugin in self.plugins:
			self.query_one(DataTable).add_row(plugin['keyword'], plugin['name'], plugin['description'])
			

		self.query_one(Input).focus()

	def compose(self) -> ComposeResult:
		"""Create child widgets for the app."""
		#yield Header()
		yield mode()
		yield Input(placeholder="Query")
		yield IndeterminateProgress()
		yield DataTable()
		yield ListView()
		yield Footer()

	def on_key(self, event: events.Key) -> None:
		log(event.key)

		if event.key == "left":
			self.query_one(Input).focus()
		elif event.key == "right":
			self.query_one(Input).focus()
		elif event.key == "up":
			self.query_one(ListView).focus()
		elif event.key == "down":
			self.query_one(ListView).focus()
		elif event.key == "ctrl+1":
			self.query_one(ListView).index = 1
			self.app.exit()
		elif event.key == "escape":
			if(self.settings['terminal'] == "windowsterminal"): pyautogui.hotkey('win', '`')
			self.app.exit()

	async def on_input_changed(self, message: Input.Changed) -> None:
		"""A coroutine to handle a text changed message."""
		self.query_one(IndeterminateProgress).visible = False

		if message.value:
			self.query_one(DataTable).display = False
			vlist = self.query_one(ListView)
			vlist.clear()

			parts = message.value.split(" ", 1)

			plugin_to_use = None
			for plugin in self.plugins:
				if parts[0] == plugin['keyword']:
					log("found plugin")
					plugin_to_use = plugin
					break

			if plugin_to_use is None:
				self.current_plugin = None
				return

			#Header update
			realtime_text = "Realtime:Enter key selects first option" if plugin['realtime'] else "Deferred:Enter key submits input query"
			self.query_one(mode).set_content(f"{chr(int(plugin['icon'], 16))} {plugin['name']} | {plugin['description']} [{realtime_text}]")

			self.current_plugin = plugin_to_use

			if self.current_plugin and self.current_plugin['realtime'] and len(parts) > 1:
				#if len(parts) > 1:
				if self.task is not None:
					self.task.cancel()
				self.task = asyncio.create_task(self.get_console_output(parts[1], plugin_to_use))
				#self.query_one(mode).reset()
				self.query_one(IndeterminateProgress).visible = True

		else:
			self.query_one(DataTable).display = True
			self.query_one(ListView).clear()
			self.query_one(IndeterminateProgress).visible = False
			self.query_one(mode).reset()
			

	async def on_input_submitted(self, event: Input.Submitted) -> None:
		#event.value
		if self.current_plugin and self.current_plugin['realtime']:
			await self.activated()
		elif self.current_plugin and not self.current_plugin['realtime']:
			#await self.get_console_output(event.value, self.current_plugin)
			log("non-realtime go: " + event.value)
			if self.task is not None:
				self.task.cancel()
			self.task = asyncio.create_task(self.get_console_output(event.value.split(" ", 1)[1], self.current_plugin))
			self.query_one(IndeterminateProgress).visible = True

	async def on_list_view_selected(self, message: ListView.Selected) -> None:
		await self.activated()

	async def get_console_output(self, query: str, plugin: dict) -> None:
		vlist = self.query_one(ListView)
		command = plugin['search'].replace("{query}", query)
		log("command: " + command)
		process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
		output, stderr = await process.communicate()
		
		if(stderr):
			log("command_error: " + str(stderr, 'utf-8'))
		#else:
			#log("command_output: " + str(output, 'utf-8'))

		try:
			self.current_object = json.loads(str(output, 'utf-8'))
			log(self.current_object)
		except json.decoder.JSONDecodeError as e:
			log(f'Error decoding JSON: {e}')
			self.query_one(IndeterminateProgress).visible = False
			return

		self.query_one(IndeterminateProgress).visible = False

		#for i, item in self.current_object.items():
			#log(item)
			#conf = item['confidence'] if 'confidence' in item else ""
			#vlist.append( ListItem(Label( f"{str(i)} : {item['name']} - {item['description']} ({conf})" )))

		for i in range(len(self.current_object)):
			log(type(self.current_object[i]))
			try: 
				log(self.current_object[i]['name'])
			except Exception as e:
				# code that will be executed if any exception is raised
				log("Error: ", e)
				continue

			obj = self.current_object[i]
			conf = obj['confidence'] if 'confidence' in obj else ""
			vlist.append( ListItem(Label( f"{str(i)} : {obj['name']} - {obj['description']} ({conf})" )))
			#print("Object at index ", i, ": ", obj["name"], " is ", obj["age"], " years old.")

	async def activated(self) -> None:
		vlist = self.query_one(ListView)
		log(vlist.index)
		log(self.current_object[vlist.index])

		index = str(vlist.index)
		action = self.current_object[vlist.index]['action']
		query = self.query_one(Input).value.split(" ", 1)[1]

		command = self.current_plugin['run'].replace("{action}", str(action)).replace("{index}", index).replace("{query}", str(query))
		log(command)

		process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
		output, stderr = await process.communicate()

		if(stderr):
			log("command_error: " + str(stderr, 'utf-8'))
		else:
			log("command_output: " + str(output, 'utf-8'))

		if self.task is not None:
			self.task.cancel()
		pyautogui.hotkey('win', '`')
		self.app.exit()

	def action_toggle_dark(self) -> None:
		"""An action to toggle dark mode."""
		self.dark = not self.dark

if __name__ == "__main__":
	app = KeyLauncher()
	app.run()