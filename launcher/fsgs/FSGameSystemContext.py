from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import hashlib

import os
import shutil
import tempfile
import time
import weakref
import threading
import traceback

import six
from fsbc.task import current_task
from fsgs.Archive import Archive
from .BaseContext import BaseContext
from .Downloader import Downloader
from .FileDatabase import FileDatabase
from .GameDatabase import GameDatabase
from .LockerDatabase import LockerDatabase


class NotFoundError(RuntimeError):
    pass


class File(object):

    def __init__(self, path):
        self.path = path


class FileContext(BaseContext):

    def __init__(self, main_context):
        BaseContext.__init__(self, main_context)

    def find_by_sha1(self, sha1):
        database = FileDatabase.instance()
        result = database.find_file(sha1=sha1)["path"]
        if not result:
            path = Downloader.get_cache_path(sha1)
            if os.path.exists(path):
                result = path
        #    result = self.context.get_game_database().find_file_by_sha1(sha1)
        # print("find by sha1", sha1, "in file database - result", result)
        if not result:
            database = LockerDatabase.instance()
            if database.check_sha1(sha1):
                result = "locker://" + sha1
            # print("find by sha1", sha1, "in locker database - result",
            # result)
        return result

    def check_sha1(self, sha1):
        database = FileDatabase.instance()
        result = database.check_sha1(sha1)
        if not result:
            database = LockerDatabase.instance()
            result = database.check_sha1(sha1)
            # print("check sha1", sha1, "in locker database - result", result)
        #if not result:
        #    result = self.context.get_game_database().find_file_by_sha1(sha1)
        return result

    def get_license_code_for_url(self, url):
        return self.context.get_game_database().get_license_code_for_url(url)

    # FIXME: better name
    def convert_uri(self, uri, prefer_path=False):
        if uri.startswith("sha1://"):
            return self.open_sha1_uri(uri)
        elif uri.startswith("db://"):
            # old name for sha1://
            return self.open_sha1_uri(uri)
        elif uri.startswith("http://"):
            return self.open_url(uri)
        elif uri.startswith("https://"):
            return self.open_url(uri)
        elif uri.startswith("locker://"):
            return self.open_locker_uri(uri)
        else:
            if prefer_path and os.path.exists(uri):
                # return helper object so isinstance does not match with str
                return File(uri)
            return Archive(uri).open(uri)

    def open(self, uri, prefer_path=False):
        while isinstance(uri, six.string_types):
            uri = self.convert_uri(uri, prefer_path=prefer_path)
        if prefer_path and isinstance(uri, File):
            # is a path
            return uri.path
        elif hasattr(uri, "read"):
            # is a file object
            return uri
        elif uri is None:
            # file was not found
            return None
        raise Exception("unexpected result in fsgs.file.open")

    def open_sha1_uri(self, uri):
        sha1 = uri.split("/")[2]
        assert len(sha1) == 40
        return self.find_by_sha1(sha1)

    def open_locker_uri(self, uri):
        sha1 = uri[9:]
        assert len(sha1) == 40

        # very ugly dependencies here...
        from .ogd.context import SynchronizerContext
        from .ogd.base import SynchronizerBase
        context = SynchronizerContext()

        fixme = SynchronizerBase(context)
        server = fixme.get_server()
        opener = fixme.get_opener()

        url = "http://{0}/api/locker/{1}".format(server, sha1)
        path = Downloader.cache_file_from_url(url, opener=opener)
        return path

    def open_url(self, url):
        original_url = url
        hash_part = ""
        parts = url.split("#", 1)
        if len(parts) > 1:
            url = parts[0]
            hash_part = "#" + parts[1]
        if not Downloader.cache_file_from_url(url, download=False):
            license_code = self.get_license_code_for_url(original_url)
            license_status = {
                "accepted": False,
                "done": False
            }

            def show_license_code():
                try:
                    try:
                        license_status["accepted"] = self.show_license_code(
                            license_code)
                    except Exception:
                        traceback.print_exc()
                finally:
                    license_status["done"] = True

            if license_code:
                print("URL", url, "has license code", license_code)
                # FIXME: remove direct dependency on fsui
                import fsui as fsui
                fsui.call_after(show_license_code)
                while not license_status["done"]:
                    time.sleep(0.1)
                if not license_status["accepted"]:
                    # FIXME: custom exception here
                    raise Exception("Usage terms \"{0}\" was not "
                                    "accepted".format(license_code))
        path = Downloader.cache_file_from_url(url)
        return path + hash_part

    def show_license_code(self, license_code):
        if license_code == "BTTR":
            license_text = (
                "Files for this game are provided by back2roots.org.\n\n"
                "By using back2roots.org or any of their services you "
                "agree to their Acceptable Usage Policy:\n\n"
                "http://www.back2roots.org/About/Project/Policy/")
        else:
            license_text = license_code
        return self.on_show_license_information(license_text)

    def on_show_license_information(self, license_text):
        print("*** on_show_license_information not implemented ***")
        raise Exception("on_show_license_information not implemented")

    def copy_game_file(self, src, dst):
        try:
            return self._copy_game_file(src, dst)
        except NotFoundError as e:
            if self.context.config.get("download_file"):
                # we should be able to find all missing files after we have
                # downloaded and extracted this archive
                self.download_game_file_archive(
                    self.context.config.get("download_file"))
                # now try to re-open the file (should be found in the cache
                return self._copy_game_file(src, dst)
            raise e

    def _copy_game_file(self, src, dst):
        ifs = self.open(src, prefer_path=True)
        if not ifs:
            raise NotFoundError("Could not find file for {0}".format(src))

        if os.path.exists(dst):
            print("removing existing file", dst)
            os.remove(dst)

        if isinstance(ifs, six.string_types):
            # we got a direct path
            try:
                os.link(ifs, dst)
                return
            except Exception:
                # couldn't link file, normal on non-unix systems and also
                # if the files are on different file systems
                pass
            shutil.copyfile(ifs, dst)
        else:
            dst_partial = dst + ".partial"
            with open(dst_partial, "wb") as ofs:
                #ifs_sha1 = hashlib.sha1()
                while True:
                    data = ifs.read()
                    if not data:
                        break
                    #ifs_sha1.update(data)
                    ofs.write(data)
            print("rename file from", dst_partial, "to", dst)
            os.rename(dst_partial, dst)

    def download_game_file_archive(self, url):
        print("\ndownload_game_file_archive", url)
        archive_path = Downloader.cache_file_from_url(url)
        archive = Archive(archive_path)
        archive_files = archive.list_files()
        print(archive_files)
        for name in archive_files:
            print(name)
            ifs = archive.open(name)
            data = ifs.read()
            Downloader.cache_data(data)
        if len(archive_files) == 0:
            # might not be an archive then
            with open(archive_path, "rb") as f:
                data = f.read()
            Downloader.cache_data(data)
        # the downloaded archive is no longer needed, now that we have
        # extracted all the files
        os.remove(archive_path)
        print("\n")


class FSGameSystemContext(object):

    def __init__(self):
        self._amiga = None
        self._config = None
        self._signal = None
        self._netplay = None
        self._game = None
        # self._variant = None
        self.file = FileContext(self)
        self.thread_local = threading.local()

    @property
    def amiga(self):
        if self._amiga is None:
            from .amiga.AmigaContext import AmigaContext
            self._amiga = AmigaContext(self)
        return self._amiga

    @property
    def config(self):
        if self._config is None:
            from .Config import Config
            self._config = Config(self)
        return self._config

    @property
    def game(self):
        if self._game is None:
            self._game = GameContext(self)
        return self._game

    #@property
    #def variant(self):
    #    if self._variant is None:
    #        self._variant = VariantContext(self)
    #    return self._variant

    @property
    def signal(self):
        if self._signal is None:
            from .SignalContext import SignalContext
            self._signal = SignalContext(self)
            #self._signal = Signal()
        return self._signal

    @property
    def netplay(self):
        if self._netplay is None:
            from .netplay.NetplayContext import NetplayContext
            self._netplay = NetplayContext(self)
        return self._netplay

    def get_game_database(self):
        if not hasattr(self.thread_local, "game_database"):
            # FIXME
            from fsgs.FSGSDirectories import FSGSDirectories
            path = os.path.join(
                FSGSDirectories.get_cache_dir(), "Games.sqlite")
            self.thread_local.game_database = GameDatabase(path)
        return self.thread_local.game_database

    @property
    def cache_dir(self):
        # FIXME: remove dependency
        from fsgs.FSGSDirectories import FSGSDirectories
        return FSGSDirectories.get_cache_dir()

    def temp_dir(self, suffix):
        return TemporaryDirectory(suffix)

    def temp_file(self, suffix):
        return TemporaryFile(suffix)


class TemporaryDirectory(object):

    def __init__(self, suffix):
        self.path = tempfile.mkdtemp(suffix="-fsgs-" + suffix)

    def __del__(self):
        self.delete()

    def delete(self):
        if os.environ.get("FSGS_KEEP_TEMP", "") == "1":
            print("NOTICE: keeping temp files around...")
            return
        if self.path:
            shutil.rmtree(self.path)
            self.path = None


class TemporaryFile(object):

    def __init__(self, suffix):
        #self.path = tempfile.mkstemp(suffix=suffix)
        self.dir_path = tempfile.mkdtemp(suffix="-fsgs-" + suffix)
        self.path = os.path.join(self.dir_path, suffix)

    def __del__(self):
        self.delete()

    def delete(self):
        if os.environ.get("FSGS_KEEP_TEMP", "") == "1":
            print("NOTICE: keeping temp files around...")
            return
        if self.path:
            os.unlink(self.path)
            self.path = None
        if self.dir_path:
            shutil.rmtree(self.dir_path)
            self.dir_path = None


class GameContext(object):

    def __init__(self, context):
        self._context = weakref.ref(context)
        self.name = ""
        self.uuid = ""
        self.variant = VariantContext()
        self.platform = GamePlatform()

    @property
    def fsgs(self):
        return self._context()

    def set_from_variant_uuid(self, variant_uuid):
        game_database = self.fsgs.get_game_database()
        values = game_database.get_game_values_for_uuid(variant_uuid)
        print("")
        for key in sorted(values.keys()):
            print(" * {0} = {1}".format(key, values[key]))
        print("")

        platform_id = values["platform"]
        self.platform.id = platform_id

        self.uuid = values["game_uuid"]
        self.name = values["game_name"]
        self.variant.uuid = variant_uuid
        self.variant.name = values["variant_name"]
        return values


class GamePlatform(object):

    def __init__(self):
        self._id = ""

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id.lower()

    id = property(get_id, set_id)

    @property
    def name(self):
        from .platform import PlatformHandler
        return PlatformHandler.get_platform_name(self._id)
        #if self._id == "atari-7800":
        #    return "Atari 7800"
        #if self._id == "amiga":
        #    return "Amiga"
        #if self._id == "cdtv":
        #    return "CDTV"
        #if self._id == "cd32":
        #    return "CD32"
        #raise Exception("Unrecognized platform ({0})".format(self._id))


class VariantContext(object):

    def __init__(self):
        self.name = ""
        self.uuid = ""
