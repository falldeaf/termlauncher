from textual.app import App, ComposeResult
from textual.widgets import Header, ListView, ListItem, Label, Footer, DataTable, Input
from textual import log
import asyncio
import subprocess
import json
import pyautogui

class KeyLauncher(App):
	"""A Textual key launcher app."""

	plugins = []
	current_object = {}
	task = None

	BINDINGS = [
		("d", "toggle_dark", "Toggle dark mode"),
		("q", "quit", "Quit the app"),
	]

	def on_mount(self) -> None:
		"""Called when the app is mounted."""
		log("mounted")
		f =open('settings.json', "r")
		self.settings = json.load(f)
		self.plugins = self.settings['plugins']
		f.close()
		log(self.plugins)

	def compose(self) -> ComposeResult:
		"""Create child widgets for the app."""
		#yield Header()
		yield Input(placeholder="Query")
		#yield DataTable()
		yield ListView()
		yield Footer()

	async def on_input_changed(self, message: Input.Changed) -> None:
		"""A coroutine to handle a text changed message."""
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
				return

			if len(parts) > 1:
				if self.task is not None:
					self.task.cancel()
				self.task = asyncio.create_task(self.get_console_output(parts[1], plugin_to_use))
			#vlist.append(ListItem(Label("📱 Foo")))
			#vlist.append(ListItem(Label("☄️ too")))
			#table = self.query_one(DataTable)
			#table.clear(columns=True)
			#table.add_column("id")
			#table.add_column("name")
			#table.add_rows(iter([("1", "foo"), ("2", "too")]))
			# Look up the word in the background
			#asyncio.create_task(self.lookup_word(message.value))
		else:
			# Clear the results
			#self.query_one("#results", Static).update()
			self.query_one(ListView).clear()

	async def on_list_view_selected(self, message: ListView.Selected) -> None:
		log("foo")
		vlist = self.query_one(ListView)
		log(vlist.index)
		pyautogui.hotkey('win', '`')
		quit()

	async def get_console_output(self, query: str, plugin: dict) -> None:
		log(query + " " + plugin['search'] + " " + plugin['keyword'])
		vlist = self.query_one(ListView)
		command = plugin['search'].replace("{query}", query)
		log(command)
		#output = subprocess.run([command], capture_output=True).stdout.decode('utf-8')
		#output = async with os.popen(command).read()
		process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
		output, stderr = await process.communicate()

		log(output)
		self.current_object = json.loads(output)
		for key in self.current_object:
			log(key)
			vlist.append(ListItem(Label(key)))
		

	def action_toggle_dark(self) -> None:
		"""An action to toggle dark mode."""
		self.dark = not self.dark

if __name__ == "__main__":
	#settings = json.load(open('settings.json'))
	#plugins = settings['plugins']
	#log(plugins)
	app = KeyLauncher()
	app.run()