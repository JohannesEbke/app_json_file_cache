from .data_cache import DataCache


class FunctionCache(DataCache):
    def __call__(self, func):
        def f(*args, **kwargs):
            key = {'args': args, 'kwargs': kwargs}
            assert args == () or kwargs == {}, 'Mixing positional and keyword arguments not supported: {}'.format(key)
            try:
                return self.get(key)
            except KeyError:
                self.store(key, func(*args, **kwargs))
                return self.get(key)

        f.clear = self.clear
        return f
