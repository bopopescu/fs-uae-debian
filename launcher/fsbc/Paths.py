from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys
import six
from fsbc.user import get_home_dir
from fsbc.util import memoize


class Paths(object):

    @staticmethod
    def str(path):
        return path.encode(sys.getfilesystemencoding())

    @staticmethod
    def encode(path):
        return path.encode(sys.getfilesystemencoding())

    @staticmethod
    def unicode(path):
        if isinstance(path, six.text_type):
            return path
        return path.decode(sys.getfilesystemencoding())

    @classmethod
    def join(cls, a, b):
        #if not a:
        #    return b
        #if a[-1] == "/" or a[-1] == "\\":
        #    return a + b
        #return a + "/" + b
        return os.path.join(a, b).replace("\\", "/")

    @classmethod
    def expand_path(cls, path, default_dir=None):
        if path and path[0] == "$":
            cmp_path = path.upper().replace("\\", "/")
            if cmp_path.startswith("$BASE/"):
                return cls.join(cls.get_base_dir(), path[6:])
            if cmp_path.startswith("$CONFIG/"):
                # FIXME: dependency loop, have FS-UAE Launcher register
                # this prefix with this class instead
                from fs_uae_launcher.Settings import Settings
                config_path = Settings.get("config_path")
                if config_path:
                    return cls.join(os.path.dirname(config_path), path[8:])
            if cmp_path.startswith("$HOME/"):
                return cls.join(cls.get_home_dir(), path[6:])
            # FIXME: $base_dir is deprecated
            if cmp_path.startswith("$BASE_DIR/"):
                return cls.join(cls.get_base_dir(), path[10:])
        elif not os.path.isabs(path) and default_dir is not None:
            return os.path.join(default_dir, path)
        return path

    @classmethod
    def contract_path(cls, path, default_dir=None, force_real_case=True):
        if path.rfind(":") > 1:
            # Checking against > index 1 to allow for Windows absolute paths
            # with drive letter and colon. If colon is later, we assume this
            # is an URI, and not a path, so we do not do anything with it
            return path
        if force_real_case:
            print("before", path)
            path = cls.get_real_case(path)
            print("after", path)
        #dir, file = os.path.split(path)
        #norm_dir = dir + "/"
        if default_dir is not None:
            default_dir += "/"
            if path.startswith(default_dir):
                return path[len(default_dir):]
        base_dir = cls.get_base_dir(slash=True)
        if path.startswith(base_dir):
            path = path.replace(base_dir, "$BASE/")
        home_dir = cls.get_home_dir(slash=True)
        if path.startswith(home_dir):
            path = path.replace(home_dir, "$HOME/")
        return path

    @classmethod
    @memoize
    def get_base_dir(cls, slash=False):
        # FIXME: dependency loop
        from fsgs.FSGSDirectories import FSGSDirectories
        path = FSGSDirectories.get_base_dir()
        if slash:
            path += "/"
        return path

    @classmethod
    @memoize
    def get_home_dir(cls, slash=False):
        path = get_home_dir()
        path = cls.get_real_case(path)
        if slash:
            path += "/"
        return path

    @classmethod
    def get_real_case(cls, path):
        """Check the case for the (case insensitive) path. Used to make the
        database portable across sensitive/insensitive file systems."""

        # not really needed on Linux

        parts = []
        drive, p = os.path.splitdrive(path)
        if path.startswith("/"):
            drive = "/"
        elif drive:
            # on Windows, add / to make drive a valid path
            drive += "/"
        last = ""
        while p != last:
            name = os.path.basename(p)
            if not name:
                break
            parts.append(name)
            last = p
            p = os.path.dirname(p)
        parts.reverse()
        #print(drive, parts)
        result = [drive]
        result.extend(parts)

        combined = drive
        combined = combined.upper()
        k = 1
        for part in parts:
            #print("part is", part)
            if os.path.isdir(combined):
                #print("checking case of", combined+ "/" + part)
                for name in os.listdir(combined):
                    if name.lower() == part.lower():
                        #print("found case =", name)
                        combined += "/" + name
                        result[k] = name
                        break
                else:
                    raise Exception("could not find case for path " + path)
            k += 1
        # normalizing slashes to forward slash to make the database more
        # portable
        result_path = os.path.join(*result).replace("\\", "/")
        return result_path
