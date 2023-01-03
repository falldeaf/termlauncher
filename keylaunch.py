from textual.app import App, ComposeResult
from textual.widgets import Header, ListView, ListItem, Label, Footer, DataTable, Input
from textual import log

class KeyLauncher(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Input(placeholder="Query")
        #yield DataTable()
        yield ListView()
        yield Footer()

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            vlist = self.query_one(ListView)
            vlist.clear()
            vlist.append(ListItem(Label("Foo")))
            vlist.append(ListItem(Label("too")))
            #table = self.query_one(DataTable)
            #table.clear(columns=True)
            #table.add_column("id")
            #table.add_column("name")
            #table.add_rows(iter([("1", "foo"), ("2", "too")]))
            # Look up the word in the background
            #asyncio.create_task(self.lookup_word(message.value))
        #else:
            # Clear the results
            #self.query_one("#results", Static).update()

    async def on_list_view_selected(self, message: ListView.Selected) -> None:
        log("foo")
        vlist = self.query_one(ListView)
        log(vlist.index)
        #quit()

    async def get_console_output():
        log("blah")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = KeyLauncher()
    app.run()