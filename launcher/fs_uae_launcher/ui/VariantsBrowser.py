from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import traceback
from fs_uae_launcher.ui.ConfigGroup import ConfigGroup

import six
from fsgs import fsgs
from fsgs.Database import Database
import fsui as fsui
from ..Config import Config
from ..Signal import Signal
from ..Settings import Settings


class LastVariants(object):

    def __init__(self):
        self.cache = {}
        Signal.add_listener("quit", self)

    def on_quit_signal(self):
        database = Database.get_instance()
        for key, value in six.iteritems(self.cache):
            database.set_last_game_variant(key, value)
        database.commit()


class VariantsBrowser(fsui.VerticalItemView):

    @staticmethod
    def use_horizontal_layout():
        return fsui.get_screen_size()[0] > 1024

    def __init__(self, parent):
        fsui.VerticalItemView.__init__(self, parent)
        self.parent_uuid = ""
        self.items = []
        #self.last_variants = LastVariants()

        self.icon = fsui.Image("fs_uae_launcher:res/fsuae_config_16.png")
        self.adf_icon = fsui.Image("fs_uae_launcher:res/adf_game_16.png")
        self.ipf_icon = fsui.Image("fs_uae_launcher:res/ipf_game_16.png")
        self.cd_icon = fsui.Image("fs_uae_launcher:res/cd_game_16.png")
        self.hd_icon = fsui.Image("fs_uae_launcher:res/hd_game_16.png")
        #self.missing_icon = fsui.Image(
        #    "fs_uae_launcher:res/missing_game_16.png")
        self.missing_icon = fsui.Image(
            "fs_uae_launcher:res/16/delete_grey.png")
        self.missing_color = fsui.Color(0xa8, 0xa8, 0xa8)

        self.blank_icon = fsui.Image(
            "fs_uae_launcher:res/16/blank.png")
        self.bullet_icon = fsui.Image(
            "fs_uae_launcher:res/16/bullet.png")

        self.manual_download_icon = fsui.Image(
            "fs_uae_launcher:res/16/arrow_down_yellow.png")
        self.auto_download_icon = fsui.Image(
            "fs_uae_launcher:res/16/arrow_down_green.png")

        self.up_icon = fsui.Image(
            "fs_uae_launcher:res/16/thumb_up_mod.png")
        self.down_icon = fsui.Image(
            "fs_uae_launcher:res/16/thumb_down_mod.png")
        self.fav_icon = fsui.Image("fs_uae_launcher:res/rating_fav_16.png")

        Settings.add_listener(self)
        Config.add_listener(self)
        self.on_setting("parent_uuid", Settings.get("parent_uuid"))

    def on_destroy(self):
        Settings.remove_listener(self)
        #Signal.remove_listener("quit", self)

    def on_select_item(self, index):
        if index is None:
            return
        self.load_variant(self.items[index])
        #self.last_variants.cache[self.parent_uuid] = variant_uuid

    def on_activate_item(self, index):
        from ..FSUAELauncher import FSUAELauncher
        FSUAELauncher.start_game()

    def on_setting(self, key, value):
        if key == "parent_uuid":
            self.parent_uuid = value
            if value:
                self.update_list(value)
            else:
                Settings.set("game_uuid", "")
                self.set_items([])

    def on_config(self, key, value):
        if key == "variant_rating":
            variant_uuid = Config.get("variant_uuid")
            for item in self.items:
                if item["uuid"] == variant_uuid:
                    item["personal_rating"] = int(value or 0)
                    self.update()

    def set_items(self, items):
        self.items = items
        self.update()

    def get_item_count(self):
        return len(self.items)

    def get_item_text(self, index):
        name = self.items[index]["name"]
        name = name.replace(", ", " \u00b7 ")
        return name

    def get_item_text_color(self, index):
        have = self.items[index]["have"]
        if not have:
            return self.missing_color

    def get_item_icon(self, index):
        have = self.items[index]["have"]
        if not have:
            #return self.missing_icon
            return self.blank_icon
        if have == 1:
            return self.manual_download_icon
        if have == 2:
            return self.auto_download_icon
        return self.get_item_extra_icons(index)[0] or self.bullet_icon
        # name = self.items[index]["name"]
        # have = self.items[index]["have"]
        # if not have:
        #     return self.missing_icon
        # if have == 1:
        #     return self.manual_download_icon
        # if have == 2:
        #     return self.auto_download_icon
        #
        # if "IPF" in name:
        #     return self.ipf_icon
        # if "ADF" in name:
        #     return self.adf_icon
        # if "WHDLoad" in name:
        #     return self.hd_icon
        # if "CD32" in name:
        #     return self.cd_icon
        # if "CDTV" in name:
        #     return self.cd_icon
        # return self.icon

    def get_item_extra_icons(self, index):
        personal_rating = self.items[index]["personal_rating"]
        if personal_rating == 5:
            return [self.fav_icon]
        elif personal_rating == 4:
            return [self.up_icon]
        elif personal_rating == 3:
            return [self.up_icon]
        elif personal_rating == 2:
            return [self.down_icon]
        elif personal_rating == 1:
            return [self.down_icon]
        return [None]

    def update_list(self, game_uuid):
        database = Database.get_instance()
        game_database = fsgs.get_game_database()
        items = database.find_game_variants_new(game_uuid, have=0)
        #items = database.search_configurations(self.search)
        sortable_items = []
        for item in items:
            name = item["name"]

            name = name.replace("\nAmiga \u00b7 ", "\n")
            #print(name, item[3])
            #name = name.replace("\nCD32 \u00b7 ", "\n")
            #name = item[1].replace("\n", " \u00b7 ")

            # only show variant name (without game name)
            name = name.split("\n", 1)[-1]

            item["like_rating"], item["work_rating"] = game_database\
                .get_ratings_for_game(item["uuid"])
            item["personal_rating"], ignored = database.get_ratings_for_game(
                item["uuid"])

            sort_key = (1 - bool(item["have"]), 1000000 - item["like_rating"],
                        1000000 - item["work_rating"], name)
            sortable_items.append(
                (sort_key, item))
        self.items = [x[1] for x in sorted(sortable_items)]
        self.update()
        #self.set_items(self.items)
        #self.set_item_count(len(self.items))

        self.select_item(None)

        select_index = None
        list_uuid = Settings.get("game_list_uuid")
        if list_uuid:
            list_variant_uuid = database.get_variant_for_list_and_game(
                list_uuid, game_uuid)
            print("game list", list_uuid, "override variant",
                  list_variant_uuid)
        else:
            list_variant_uuid = None
        if list_variant_uuid:
            # override variant selection from list if possible
            for i, item in enumerate(self.items):
                print(item["uuid"], item["name"], list_variant_uuid)
                if item["uuid"] == list_variant_uuid:
                    select_index = i
                    print("override select index", select_index)
                    break
        if select_index is None:
            # default index selection
            for i, item in enumerate(self.items):
                if item["personal_rating"] == 5:
                    select_index = i
                    break
            else:
                if len(self.items) > 0:
                    select_index = 0

        if select_index is not None:
            print("selecting variant index", select_index)
            self.select_item(select_index)
        else:
            ConfigGroup.new_config()

        # try:
        #     variant_uuid = self.last_variants.cache[game_uuid]
        # except KeyError:
        #     variant_uuid = database.get_last_game_variant(game_uuid)
        # if len(self.items) > 0:
        #     for i, item in enumerate(self.items):
        #         if item[3] == variant_uuid:
        #             self.select_item(i)
        #             break
        #     else:
        #         self.select_item(0)

    def load_variant(self, item):
        try:
            self._load_variant(item)
        except Exception:
            traceback.print_exc()
            Config.load_default_config()
            Config.load({
                "__error": ("Error loading configuration\n"
                            "See log file for details.")
            })
            self.select_item(None)

    def _load_variant(self, item):
        variant_uuid = item["uuid"]
        game_database = fsgs.get_game_database()
        # game_database_client = GameDatabaseClient(game_database)
        # try:
        #     variant_id = game_database_client.get_game_id(variant_uuid)
        # except Exception:
        #     # game not found:
        #     print("could not find game", repr(variant_uuid))
        #     Config.load_default_config()
        #     return
        # values = game_database_client.get_final_game_values(variant_id)
        try:
            values = game_database.get_game_values_for_uuid(variant_uuid)
        except Exception:
            # game not found:
            traceback.print_exc()
            print("could not find game", repr(variant_uuid))
            Config.load_default_config()
            return

        #values["variant_uuid"] = variant_uuid
        #values["variant_rating"] = str(item["personal_rating"])

        print(values)
        Config.load_values(values, uuid=variant_uuid)

        #variant_rating = 0
        #if item["work_rating"] is not None:
        #    variant_rating = item["work_rating"] - 2
        #if item["like_rating"]:
        #    variant_rating = item["like_rating"]
        #Config.set("__variant_rating", str(variant_rating))

        Config.set("variant_uuid", variant_uuid)
        Config.set("variant_rating", str(item["personal_rating"]))
        Config.set("__changed", "0")
