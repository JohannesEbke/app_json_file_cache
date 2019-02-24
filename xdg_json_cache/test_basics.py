from . import cache_for_app

Cache = cache_for_app("xdg_json_cache")


def test_simple():
    assert Cache("test_simple")(lambda: 12)() == 12
    assert Cache("test_simple")(lambda: 13)() == 12


def test_vary():
    assert Cache("test_simple", vary=1)(lambda: 12)() == 12
    assert Cache("test_simple", vary=2)(lambda: 13)() == 13


def test_corrupt():
    assert Cache("test_simple", vary=1)(lambda: 12)() == 12
    with open(Cache("test_simple").filename, "w") as fd:
        fd.write("not JSON")
    assert Cache("test_simple", vary=1)(lambda: 24)() == 24
