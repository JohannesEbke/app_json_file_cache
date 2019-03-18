from hashlib import sha512
from json import dump, dumps, load
from os import makedirs
from os.path import join as pjoin
from shutil import rmtree

from appdirs import user_cache_dir


class DataCache:
    def __init__(self, app_name, function_name, vary=None):
        self.filepath = pjoin(user_cache_dir(app_name), function_name)
        self.vary = vary
        self._data = {}
        self.version = 1

    def get(self, key):
        key_string = self._key_to_string(key)
        if key_string not in self._data:
            try:
                data = load(open(self._filename(key_string)))
                if data['version'] == self.version and data['vary'] == self.vary:
                    self._data[key_string] = data
            except (ValueError, OSError, IOError, KeyError):
                pass
        return self._data[key_string]['data']

    def store(self, key, data):
        key_string = self._key_to_string(key)
        try:
            makedirs(self.filepath)
        except OSError:
            pass
        self._data[key_string] = {'version': self.version, 'data': data, 'vary': self.vary}
        dump(self._data[key_string], open(self._filename(key_string), "w"))

    def clear(self):
        rmtree(self.filepath)

    def _filename(self, key_string):
        return pjoin(self.filepath, sha512(key_string.encode('utf-8')).hexdigest() + ".json")

    def _key_to_string(self, key):
        return dumps(key, sort_keys=True)
