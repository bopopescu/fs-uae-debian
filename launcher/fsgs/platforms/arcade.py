from fsgs.platform import PlatformHandler
from fsgs.mame.arcade import ArcadeRunner
from .loader import SimpleLoader


class ArcadePlatformHandler(PlatformHandler):

    PLATFORM_NAME = "Arcade"

    def __init__(self):
        PlatformHandler.__init__(self)

    def get_loader(self, fsgs):
        return ArcadeLoader(fsgs)

    def get_runner(self, fsgs):
        return ArcadeRunner(fsgs)


class ArcadeLoader(SimpleLoader):

    def load_files(self, values):
        # file_list = json.loads(values["file_list"])
        # assert len(file_list) == 1
        # self.config["cartridge"] = "sha1://{0}/{1}".format(
        #     file_list[0]["sha1"], file_list[0]["name"])
        self.config["file_list"] = values["file_list"]

    def load_extra(self, values):
        if "refresh_rate" in values:
            self.config["refresh_rate"] = values["refresh_rate"]
        self.config["mame_rom_set"] = values["mame_rom_set"]
