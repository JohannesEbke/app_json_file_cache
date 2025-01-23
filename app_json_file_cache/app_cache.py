from .function_cache import FunctionCache


class AppCache:

    def __init__(self, app_name):
        self.app_name = app_name

    def __call__(self, name, vary=None, cheap_default_func=None):
        return FunctionCache(self.app_name, name, vary, cheap_default_func=cheap_default_func)
