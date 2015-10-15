import os
from fsgs.FSGSDirectories import FSGSDirectories
from .GameNameUtil import GameNameUtil


class SaveStateHandler(object):

    def __init__(self, fsgs, name, platform, uuid=None):
        self.fsgs = fsgs
        self.uuid = uuid

        self.config_name = name
        if "(" in name:
            parts = name.split("(", 1)
            self.name, self.variant = parts
            self.name = self.name.strip()
            self.variant = self.variant.strip()
            if self.variant.endswith(")"):
                self.variant = self.variant[:-1]
            self.variant = self.variant.replace(") (", ", ")
            self.variant = self.variant.replace(")(", ", ")
        else:
            self.name = name
            self.variant = ""
        self.platform = platform

    def get_name(self):
        return self.name

    def get_variant(self):
        return self.variant

    def _get_state_dir(self):
        config_name = self.config_name
        if not config_name:
            config_name = "Default"

        # use a temporary state dir, for now, to avoid problems with
        # floppy overlays etc interfering with net play
        if self.fsgs.netplay.enabled:
            # it is possible to manually specify the state dir
            config_name = self.fsgs.config.get("__netplay_state_dir_name")
            if not config_name:
                # this is the default behavior, create a clean state
                # dir for the net play session
                netplay_game = self.fsgs.config.get("__netplay_game")
                if netplay_game:
                    config_name = "Net Play ({0})".format(netplay_game)

        # convert the config name to a name which can be represented on
        # the file system (really all/most filesystems).
        config_name = GameNameUtil.create_fs_name(config_name)

        letter = self.get_letter(config_name)
        if not letter:
            config_name = "Default"
            letter = self.get_letter(config_name)
        # we use an existing state dir in a "letter" dir if it exists
        # (legacy support).
        path = os.path.join(
            FSGSDirectories.get_save_states_dir(), letter, config_name)
        if os.path.exists(path):
            return path
        # if not, we use a direct subfolder of save states dir
        path = os.path.join(
            FSGSDirectories.get_save_states_dir(), config_name)
        return path

    def get_state_dir(self):
        state_dir = self._get_state_dir()
        if not os.path.exists(state_dir):
            os.makedirs(state_dir)
        return state_dir

    @staticmethod
    def get_letter(name):
        letter_name = name.upper()
        if letter_name.startswith("THE "):
            letter_name = letter_name[4:]
        if letter_name.startswith("A "):
            letter_name = letter_name[2:]
        for i in range(len(letter_name)):
            letter = letter_name[i]
            if letter in "01234567890":
                letter = "0"
                break
            if letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                break
        else:
            return None
        return letter
