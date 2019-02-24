from json import dump, load
from json.decoder import JSONDecodeError
from functools import partial
from os import getenv, makedirs
from os.path import expandvars
from os.path import join as pjoin

XDG_CACHE_HOME = getenv('XDG_CACHE_HOME', default=expandvars(pjoin('$HOME', '.cache')))

class Cache:
    def __init__(self, app, name, vary=None):
        self.filepath = pjoin(XDG_CACHE_HOME, app)
        self.filename = pjoin(self.filepath, name + ".json")
        self.vary = vary
        self._data = None

    def __call__(self, func):
        def f():
            data = self._get_data()
            if data is None:
                result = func()
                data = self._store_result(result)
            return data['result']

        return f

    def _get_data(self):
        if self._data is None:
            self._load_data()
        return self._data

    def _load_data(self):
        try:
            data = load(open(self.filename))
            if data.get('version') == 1 and data.get('vary') == self.vary:
                self._data = data
        except (JSONDecodeError, FileNotFoundError):
            pass

    def _store_result(self, result):
        makedirs(self.filepath, exist_ok=True)
        self._data = {'version': 1, 'result': result, 'vary': self.vary}
        dump(self._data, open(self.filename, "w"))
        return self._data


cache_for_app = lambda app_name: partial(Cache, app_name)
