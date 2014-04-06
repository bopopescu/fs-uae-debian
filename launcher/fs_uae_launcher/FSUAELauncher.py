from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys
import shutil
import hashlib
import traceback
from collections import defaultdict
from fs_uae_launcher.ui.download import DownloadGameWindow, DownloadTermsDialog
from fsgs.Downloader import Downloader
import six
from fs_uae_launcher.PluginHelper import PluginHelper
from fsbc.Application import app
from fsbc.configparser import ConfigParser, NoSectionError
from fsbc.system import windows, macosx
from fsbc.task import Task
from fsgs.application import ApplicationMixin
from fsgs.input.helper import DeviceHelper
from fsgs.platform import PlatformHandler
import fsbc.fs as fs
import fsui as fsui
from fsgs import fsgs
from fsgs.Database import Database
from .ui.MainWindow import MainWindow

from fsgs.FileDatabase import FileDatabase
from fsbc.Paths import Paths
from fsgs.amiga.Amiga import Amiga
from fsgs.amiga.ROMManager import ROMManager

from .Config import Config
from .ConfigurationScanner import ConfigurationScanner
from fsgs.FSGSDirectories import FSGSDirectories
from .I18N import _, gettext, initialize_locale
from .Settings import Settings
from .UpdateManager import UpdateManager


class FSUAELauncher(ApplicationMixin, fsui.Application):

    def __init__(self):
        fsui.Application.__init__(self, "fs-uae-launcher")
        self.set_icon(fsui.Icon("fs-uae-launcher", "pkg:fs_uae_launcher"))

        if fsui.use_qt:
            from fsui.qt import QStyleFactory
            self.qapplication.setStyle(QStyleFactory.create("Fusion"))

            plugin_helper = PluginHelper()
            for res in plugin_helper.find_resource_dirs(
                    "fs-uae-launcher-theme"):
                qt_css = os.path.join(res, "stylesheet.qss")
                if os.path.exists(qt_css):
                    with open(qt_css, "rb") as f:
                        data = f.read()
                    self.qapplication.setStyleSheet(data)

    @staticmethod
    def get_game_database_path():
        launcher_dir = FSGSDirectories.get_launcher_dir()
        path = os.path.join(launcher_dir, "Game Database.sqlite")
        return path

    #noinspection PyMethodMayBeStatic
    def on_idle(self):
        fsgs.signal.process()

    def start(self):
        print("FSUAELauncherApplication.start")

        # GameDatabase.set_database_path(self.get_game_database_path())
        # OverlayDatabase.set_database_path(self.get_overlay_database_path())

        self.parse_arguments()
        self.load_settings()

        language = Settings.get("language")
        initialize_locale(language)

        self.config_startup_scan()
        self.kickstart_startup_scan()

        #sys.exit(1)

        # FIXME: should now sanitize check some options -for instance,
        # - check if configured joysticks are still connected
        # - check if paths still exists, etc

        #Config.update_kickstart()

        icon = None

        def check_icon(path):
            path = os.path.join(path, "fs-uae-launcher.ico")
            if os.path.exists(path):
                return path
            return None

        if not icon:
            icon = check_icon("share/fs-uae-launcher")
        if not icon:
            icon = check_icon("launcher/share/fs-uae-launcher")
        # FIXME: should check data directories (XDG_DATA_DIRS) properly
        # instead
        if not icon:
            # this encoding / decoding is a bit ridiculous, but, this is
            # for Python 2.x..
            icon = check_icon(os.path.expanduser(
                "~/.local/share/fs-uae-launcher".encode(
                    sys.getfilesystemencoding())).decode(
                sys.getfilesystemencoding()))
        if not icon:
            icon = check_icon("/usr/local/share/fs-uae-launcher")
        if not icon:
            icon = check_icon("/usr/share/fs-uae-launcher")
        if macosx:
            # Icons come from the app bundles
            icon = None

        plugins_dir = FSGSDirectories.get_plugins_dir()
        if plugins_dir:
            dont_write_bytecode = sys.dont_write_bytecode
            try:
                self.load_plugins(plugins_dir)
            finally:
                sys.dont_write_bytecode = dont_write_bytecode

        window = MainWindow(icon=icon)
        MainWindow.instance = window
        window.show()

        if "--workspace" in sys.argv:
            window.set_position((300, 200))

            from fs_uae_workspace.desktop import get_desktop_window
            get_desktop_window()

        UpdateManager.run_update_check()

    @staticmethod
    def load_plugins(plugins_dir):
        print("loading plugins")
        for full_name in os.listdir(plugins_dir):
            name, ext = os.path.splitext(full_name)
            if ext.lower() != ".py":
                continue
            path = os.path.join(plugins_dir, full_name)
            print("loading", path)
            name = "plugin_" + hashlib.sha1(path.encode("UTF-8")).hexdigest()
            print(name)
            import imp
            try:
                #with open(path, "r") as f:
                #    plugin = imp.load_source(name, name, f)
                plugin = imp.load_source(
                    name, path.encode(sys.getfilesystemencoding()))
                print("name:", getattr(plugin, "name", ""))
                print("version:", getattr(plugin, "version", ""))
                plugin.fsgs = fsgs
                plugin.plugin_dir = os.path.dirname(path)
                plugin.fsgs_init()
            except Exception:
                traceback.print_exc()
                continue

    def load_settings(self):
        path = app.get_settings_path()
        print("loading last config from " + repr(path))
        if not os.path.exists(path):
            print("settings file does not exist")
        if six.PY3:
            # noinspection PyArgumentList
            cp = ConfigParser(interpolation=None)
        else:
            cp = ConfigParser()
        try:
            cp.read([path])
        except Exception as e:
            print(repr(e))
            return

        config = {}
        try:
            keys = cp.options("config")
        except NoSectionError:
            keys = []
        for key in keys:
            config[key] = fs.from_utf8_str(cp.get("config", key))
        for key, value in six.iteritems(config):
            print("loaded", key, value)
            fsgs.config.values[key] = value

        #settings = {}
        #try:
        #    keys = cp.options("settings")
        #except configparser.NoSectionError:
        #    keys = []
        #for key in keys:
        #    settings[key] = fs.from_utf8_str(cp.get("settings", key))
        #for key, value in six.iteritems(settings):
        #    #if key in Settings.settings:
        #    #    # this setting is already initialized, possibly via
        #    #    # command line arguments
        #    #    pass
        #    #else:
        #
        #    #Settings.settings[key] = value
        #
        #    # FIXME: setting values directly in settings dict
        #    app.settings.values[key] = value
        #
        ##Settings.set("config_search", "")

    def parse_arguments(self):
        pass
        #for arg in sys.argv:
        #    if arg.startswith("--"):
        #        if "=" in arg:
        #            key, value = arg[2:].split("=", 1)
        #            key = key.replace("-", "_")
        #            if key == "base_dir":
        #                Settings.set("base_dir", value)

    def save_settings(self):
        path = app.get_settings_path()
        path += ".part"
        print("writing " + repr(path))

        if six.PY3:
            # noinspection PyArgumentList
            cp = ConfigParser(interpolation=None)
        else:
            cp = ConfigParser()
        cp.add_section("settings")

        for key, value in six.iteritems(app.settings.values):
            #lines.append("{0} = {1}".format(key, value))
            cp.set("settings", str(key), fs.to_utf8_str(value))

        cp.add_section("config")
        #lines.append("[config]")

        for key, value in six.iteritems(fsgs.config.values):
            if key.startswith("__"):
                # keys starting with __ are never saved
                continue
            cp.set("config", str(key), fs.to_utf8_str(value))

        if six.PY3:
            # noinspection PyArgumentList
            with open(path, "w", encoding="UTF-8", newline="\n") as f:
                cp.write(f)
        else:
            with open(path, "w") as f:
                cp.write(f)
        print("moving to " + repr(app.get_settings_path()))
        shutil.move(path, app.get_settings_path())

    @staticmethod
    def get_dir_mtime_str(path):
        try:
            return str(int(os.path.getmtime(path)))
        except Exception:
            return "0"

    def config_startup_scan(self):
        configs_dir = FSGSDirectories.get_configurations_dir()
        print("config_startup_scan", configs_dir)
        print(Settings.settings)
        settings_mtime = Settings.get("configurations_dir_mtime")
        dir_mtime = self.get_dir_mtime_str(configs_dir)
        if settings_mtime == dir_mtime:
            print("... mtime not changed", settings_mtime, dir_mtime)
            return
        database = Database.get_instance()
        file_database = FileDatabase.get_instance()

        print("... database.find_local_configurations")
        local_configs = Database.get_instance().find_local_configurations()
        print("... walk configs_dir")
        for dir_path, dir_names, file_names in os.walk(configs_dir):
            for file_name in file_names:
                if not file_name.endswith(".fs-uae"):
                    continue
                path = Paths.join(dir_path, file_name)
                if path in local_configs:
                    local_configs[path] = None
                    # already exists in database
                    continue
                name, ext = os.path.splitext(file_name)
                #search = ConfigurationScanner.create_configuration_search(
                # name)
                scanner = ConfigurationScanner()
                print("[startup] adding config", path)
                file_database.delete_file(path=path)
                with open(path, "rb") as f:
                    sha1 = hashlib.sha1(f.read()).hexdigest()
                file_database.add_file(path=path, sha1=sha1)

                game_id = database.add_game(
                    path=path, name=scanner.create_configuration_name(name))
                database.update_game_search_terms(
                    game_id, scanner.create_search_terms(name))

        for path, id in six.iteritems(local_configs):
            if id is not None:
                print("[startup] removing configuration", path)
                database.delete_game(id=id)
                file_database.delete_file(path=path)
        print("... commit")
        database.commit()
        Settings.set("configurations_dir_mtime",
                     self.get_dir_mtime_str(configs_dir))

    def kickstart_startup_scan(self):
        print("kickstart_startup_scan")
        kickstarts_dir = FSGSDirectories.get_kickstarts_dir()
        if Settings.get("kickstarts_dir_mtime") == \
                self.get_dir_mtime_str(kickstarts_dir):
            print("... mtime not changed")
        else:
            file_database = FileDatabase.get_instance()
            print("... database.find_local_roms")
            local_roms = file_database.find_local_roms()
            print("... walk kickstarts_dir")
            for dir_path, dir_names, file_names in os.walk(kickstarts_dir):
                for file_name in file_names:
                    if not file_name.endswith(".rom"):
                        continue
                    path = Paths.join(dir_path, file_name)
                    if path in local_roms:
                        local_roms[path] = None
                        # already exists in database
                        continue
                    print("[startup] adding kickstart", path)
                    ROMManager.add_rom_to_database(path, file_database)
            print(local_roms)
            for path, id in six.iteritems(local_roms):
                if id is not None:
                    print("[startup] removing kickstart", path)
                    file_database.delete_file(id=id)
            print("... commit")
            file_database.commit()
            Settings.set(
                "kickstarts_dir_mtime",
                self.get_dir_mtime_str(kickstarts_dir))

        amiga = Amiga.get_model_config("A500")
        for sha1 in amiga["kickstarts"]:
            if fsgs.file.find_by_sha1(sha1=sha1):
                break
        else:
            file_database = FileDatabase.get_instance()
            self.amiga_forever_kickstart_scan()
            file_database.commit()

    def amiga_forever_kickstart_scan(self):
        if windows:
            print("amiga forever kickstart scan")
            # noinspection PyUnresolvedReferences
            from win32com.shell import shell, shellcon
            path = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_DOCUMENTS, 0, 0)
            path = os.path.join(path, "Amiga Files", "Shared", "rom")
            self.scan_dir_for_kickstarts(path)

    @staticmethod
    def scan_dir_for_kickstarts(scan_dir):
        file_database = FileDatabase.get_instance()
        for dir_path, dir_names, file_names in os.walk(scan_dir):
            for file_name in file_names:
                if not file_name.endswith(".rom"):
                    continue
                path = Paths.join(dir_path, file_name)
                if file_database.find_file(path=path):
                #if path in local_roms:
                #    local_roms[path] = None
                #    # already exists in database
                    continue
                print("[startup] adding kickstart", path)
                ROMManager.add_rom_to_database(path, file_database)

    @classmethod
    def start_game(cls):
        from .netplay.Netplay import Netplay
        if Netplay.game_channel:
            Netplay.start_netplay_game()
        else:
            cls.start_local_game()

    @classmethod
    def start_local_game(cls):
        print("START LOCAL GAME")
        print("x_missing_files", Config.get("x_missing_files"))

        if Config.get("x_missing_files"):
            if Config.get("download_file"):
                if Config.get("download_terms") and not \
                        Downloader.check_terms_accepted(
                        Config.get("download_file"),
                        Config.get("download_terms")):
                    from .ui.MainWindow import MainWindow
                    dialog = DownloadTermsDialog(MainWindow.instance, fsgs)
                    if not dialog.show_modal():
                        return

            elif Config.get("download_page"):
                from .ui.MainWindow import MainWindow
                #fsui.show_error(_("This game must be downloaded first."))
                DownloadGameWindow(MainWindow.instance, fsgs).show()
                return
            else:
                fsui.show_error(
                    _("This game variant cannot be started "
                      "because you don't have all required files."))
                return

        platform_id = Config.get("platform")
        amiga_platform = platform_id in ["", "amiga", "cdtv", "cd32"]
        if amiga_platform:
            cls.start_local_game_amiga()
        else:
            cls.start_local_game_other()

    @classmethod
    def start_local_game_other(cls):
        variant_uuid = Config.get("variant_uuid")
        assert variant_uuid

        fsgs.game.set_from_variant_uuid(variant_uuid)
        platform_handler = PlatformHandler.create(fsgs.game.platform.id)
        runner = platform_handler.get_runner(fsgs)

        task = RunnerTask(runner)
        from .ui.LaunchDialog import LaunchDialog
        from .ui.MainWindow import MainWindow
        dialog = LaunchDialog(
            MainWindow.instance, gettext("Launching Game"), task)
        task.start()
        dialog.show_modal()
        dialog.close()

    @classmethod
    def start_local_game_amiga(cls):
        # make sure x_kickstart_file is initialized
        Config.set_kickstart_from_model()

        if not Config.get("x_kickstart_file"):  # or not \
            #  os.path.exists(Config.get("kickstart_file")):
            fsui.show_error(_("No kickstart found for this model. "
                              "Use the 'Import Kickstarts' function from "
                              "the menu."))
            return
        cs = Amiga.get_model_config(Config.get("amiga_model"))["ext_roms"]
        if len(cs) > 0:
            # extended kickstart ROM is needed
            if not Config.get("x_kickstart_ext_file"):
                fsui.show_error(_("No extended kickstart found for this "
                                  "model. Try 'scan' function."))
                return

        config = Config.copy()
        prepared_config = cls.prepare_config(config)

        model = Config.get("amiga_model")
        if model.startswith("CD32"):
            platform = "CD32"
        elif model == "CDTV":
            platform = "CDTV"
        else:
            platform = "Amiga"
        name = Settings.get("config_name")
        uuid = Config.get("x_game_uuid")
        
        from fsgs.SaveStateHandler import SaveStateHandler
        save_state_handler = SaveStateHandler(fsgs, name, platform, uuid)

        from fsgs.amiga.LaunchHandler import LaunchHandler
        launch_handler = LaunchHandler(fsgs, name, prepared_config,
                                       save_state_handler)

        from .ui.LaunchDialog import LaunchDialog
        from .ui.MainWindow import MainWindow
        task = AmigaLaunchTask(launch_handler)
        #dialog = LaunchDialog(MainWindow.instance, launch_handler)
        dialog = LaunchDialog(
            MainWindow.instance, gettext("Launching FS-UAE"), task)

        def on_show_license_information(license_text):
            # FIXME: don't depend on wx here
            # noinspection PyUnresolvedReferences
            #import wx
            #license_dialog = wx.MessageDialog(
            #    dialog, license_text, _("Terms of Use"),
            #    wx.OK | wx.CANCEL | wx.CENTRE)
            #license_dialog.CenterOnParent()
            #result = license_dialog.ShowModal()
            #return result == wx.ID_OK
            # FIXME
            return True
        fsgs.file.on_show_license_information = on_show_license_information

        task.start()
        dialog.show_modal()
        dialog.close()

    @classmethod
    def prepare_config(cls, original_config):
        config = defaultdict(six.text_type)
        for key, value in six.iteritems(app.settings.values):
            if key in Config.config_keys:
                print("... ignoring config key from settings:", key)
                continue
            config[key] = value

        config["base_dir"] = FSGSDirectories.get_base_dir()

        for key, value in six.iteritems(original_config):
            config[key] = value

        if not config["joystick_port_0_mode"]:
            config["joystick_port_0_mode"] = "mouse"
        if not config["joystick_port_1_mode"]:
            if config["amiga_model"].startswith("CD32"):
                config["joystick_port_1_mode"] = "cd32 gamepad"
            else:
                config["joystick_port_1_mode"] = "joystick"
        if not config["joystick_port_2_mode"]:
            config["joystick_port_2_mode"] = "none"
        if not config["joystick_port_3_mode"]:
            config["joystick_port_3_mode"] = "none"

        from .DeviceManager import DeviceManager
        devices = DeviceManager.get_devices_for_ports(config)
        for port in range(4):
            key = "joystick_port_{0}".format(port)
            if not config.get(key):
                # key not set, use calculated default value
                config[key] = devices[port].id

        for remove_key in ["database_username", "database_password",
                           "database_username", "database_email",
                           "database_auth", "device_id"]:
            if remove_key in config:
                del config[remove_key]

        # overwrite netplay config
        if config.get("__netplay_host", ""):
            config["netplay_server"] = config["__netplay_host"]
        if config.get("__netplay_password", ""):
            config["netplay_password"] = config["__netplay_password"]
        if config.get("__netplay_port", ""):
            config["netplay_port"] = config["__netplay_port"]

        # copy actual kickstart options from x_ options
        config["kickstart_file"] = config["x_kickstart_file"]
        config["kickstart_ext_file"] = config["x_kickstart_ext_file"]

        # make sure FS-UAE does not load other config files (Host.fs-uae)
        config["end_config"] = "1"

        # set titles
        #if not config["sub_title"]:
        #    config["sub_title"] = config["amiga_model"] or "A500"

        if config.get("__netplay_game", ""):
            print("\nfixing config for netplay game")
            for key in [x for x in config.keys() if x.startswith("uae_")]:
                print("* removing option", key)
                del config[key]
        return config


# FIXME: Files to clean up:
# Documents/FS-UAE/Cache/File Database.sqlite
# Documents/FS-UAE/Data/Game Database.sqlite
# Documents/FS-UAE/Data/Launcher.sqlite
# Documents/FS-UAE/Logs/FS-UAE.log
# Documents/FS-UAE/Logs/FS-UAE.log.txt


class AmigaLaunchTask(Task):

    def __init__(self, launch_handler):
        Task.__init__(self, "Amiga Launch Task")
        self.launch_handler = launch_handler

    def run(self):
        self.launch_handler.run_sequence()


class RunnerTask(Task):

    def __init__(self, runner):
        Task.__init__(self, "Runner Task")
        self.runner = runner

    def run(self):
        device_helper = DeviceHelper()
        device_helper.default_port_selection(self.runner.ports)

        self.runner.prepare()
        process = self.runner.run()
        process.wait()
        self.runner.finish()
