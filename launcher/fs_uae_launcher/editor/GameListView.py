from fsbc.util import unused
from fsgs.Database import Database
import fsui as fsui


class GameListView(fsui.ListView):

    def __init__(self, parent):
        fsui.ListView.__init__(self, parent)
        self.items = []

    def on_select_item(self, index):
        # index = self.get_index()
        database = Database.get_instance()
        info = database.get_game_info(self.items[index][0])
        self.set_game_info(info)

    def set_items(self, items):
        self.items = items
        self.set_item_count(len(self.items))

    def on_get_item_text(self, row, column):
        unused(column)
        return self.items[row][1]

    def on_get_item_tooltip(self, row, column):
        unused(column)
        return self.items[row][1]

    def search(self, search):
        print("search for", search)

        database = Database.get_instance()
        items = database.search_games(search)
        self.set_items(items)
