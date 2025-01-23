from . import AppCache

Cache = AppCache("app_json_file_cache")


def test_default_recalculate():

    def default_func():
        return 42

    cache = Cache("test_default_function", cheap_default_func=default_func)
    cache.clear()

    @cache
    def wrapped():
        return 12

    assert wrapped() == 42
    wrapped.recalculate()
    assert wrapped() == 12

    cache.clear()


def test_default_with_parameters_recalculate():

    def default_func(_):
        return 42

    cache = Cache("test_default_function", cheap_default_func=default_func)
    cache.clear()

    @cache
    def wrapped(x):
        return 2 * x

    assert wrapped(2) == 42
    wrapped.recalculate(2)
    assert wrapped(2) == 4
    assert wrapped(3) == 42
    assert wrapped(4) == 42
    wrapped.recalculate(4)
    assert wrapped(4) == 8

    cache.clear()
