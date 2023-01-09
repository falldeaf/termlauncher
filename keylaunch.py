import os
from textual.app import App, ComposeResult
from textual.widgets import Header, ListView, ListItem, Label, Footer, DataTable, Input, Static
from textual import log, events
import asyncio
import subprocess
import json
import pyautogui

class mode(Static):

	def on_mount(self) -> None:
		self.reset()

	def reset(self) -> None:
		self.update('(l)auncher')

	def on_click(self) -> None:
		self.next_word()

	def set_content(self, content) -> None:
		"""Get a new hello and update the content area."""
		self.update(f"{content}, [b](l)auncher[/b]")

class KeyLauncher(App):
	"""A Textual key launcher app."""

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
		log("mounted")
		script_directory = os.path.dirname(os.path.realpath(__file__))

		f =open(script_directory + '\settings.json', "r")
		self.settings = json.load(f)
		self.plugins = self.settings['plugins']
		f.close()
		log(self.plugins)
		self.query_one(Input).focus()

	def compose(self) -> ComposeResult:
		"""Create child widgets for the app."""
		#yield Header()
		yield mode()
		yield Input(placeholder="Query")
		#yield DataTable()
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
		elif event.key == "escape":
			pyautogui.hotkey('win', '`')
			self.app.exit()

	async def on_input_changed(self, message: Input.Changed) -> None:
		"""A coroutine to handle a text changed message."""
		self.query_one(mode).reset()
		
		#if self.current_plugin is not None and not self.current_plugin['realtime']:
			#return

		if message.value:
			vlist = self.query_one(ListView)
			vlist.clear()

			parts = message.value.split(" ", 1)

			plugin_to_use = None
			for plugin in self.plugins:
				if parts[0] in plugin['keyword']:
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

		else:
			self.query_one(ListView).clear()

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

	async def on_list_view_selected(self, message: ListView.Selected) -> None:
		await self.activated()

	async def get_console_output(self, query: str, plugin: dict) -> None:
		log(query + " " + plugin['search'] + " " + plugin['keyword'])
		vlist = self.query_one(ListView)
		command = plugin['search'].replace("{query}", query)
		log(command)
		#output = subprocess.run([command], capture_o``utput=True).stdout.decode('utf-8')
		#output = async with os.popen(command).read()
		process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
		output, stderr = await process.communicate()

		self.current_object = json.loads(output)
		log(self.current_object)

		for i, item in enumerate(self.current_object):
			vlist.append( ListItem(Label( f"{str(i)} : {item['name']} - {item['description']} ({item['confidence']})" )))

	async def activated(self) -> None:
		vlist = self.query_one(ListView)
		log(vlist.index)
		log(list(self.current_object.items())[vlist.index][0])

		command = self.current_plugin['run'].replace("{action}", "\"" + list(self.current_object.items())[vlist.index][0] + "\"").replace("{index}", str(vlist.index)).replace("{query}", self.query_one(Input).value.split(" ", 1)[1])

		process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
		output, stderr = await process.communicate()

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