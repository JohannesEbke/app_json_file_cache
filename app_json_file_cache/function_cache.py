from functools import partial

from .data_cache import DataCache


class FunctionCache(DataCache):
    def __init__(self, *args, **kwargs):
        cheap_default_func = kwargs.pop("cheap_default_func")
        super(FunctionCache, self).__init__(*args, **kwargs)
        self._cheap_default_func = cheap_default_func

    def __call__(self, func):
        def f(*args, **kwargs):
            key = {'args': args, 'kwargs': kwargs}
            assert args == () or kwargs == {}, 'Mixing positional and keyword arguments not supported: {}'.format(key)
            try:
                return self.get(key)
            except KeyError:
                if self._cheap_default_func:
                    return self._cheap_default_func(*args, **kwargs)
            self.store(key, func(*args, **kwargs))
            return self.get(key)

        f.clear = self.clear
        f.recalculate = partial(self.recalculate, func)
        return f

    def recalculate(self, func, *args, **kwargs):
        key = {'args': args, 'kwargs': kwargs}
        assert args == () or kwargs == {}, 'Mixing positional and keyword arguments not supported: {}'.format(key)
        self.store(key, func(*args, **kwargs))
