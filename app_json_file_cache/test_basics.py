from os.path import exists

from . import AppCache

Cache = AppCache("app_json_file_cache")


def test_simple():
    assert Cache("test_simple")(lambda: 12)() == 12
    assert Cache("test_simple")(lambda: 13)() == 12
    Cache("test_simple").clear()


def test_vary():
    assert Cache("test_simple", vary=1)(lambda: 12)() == 12
    assert Cache("test_simple", vary=2)(lambda: 13)() == 13
    Cache("test_simple").clear()


def test_corrupt():
    assert Cache("test_simple", vary=1)(lambda: 12)() == 12
    c = Cache("test_simple")
    fn = c._filename(c._key_to_string({'args': [], 'kwargs': {}}))
    assert exists(fn)
    with open(fn, "w") as fd:
        fd.write("not JSON")
    assert Cache("test_simple", vary=1)(lambda: 24)() == 24

    Cache("test_simple")(lambda: 24).clear()
    assert not exists(fn)


def test_parameter():
    cached_f = Cache("test_parameter")(lambda x: x * 2)

    assert cached_f(4) == 8
    assert cached_f(5) == 10

    cached_f2 = Cache("test_parameter")(lambda x: x * 4)
    assert cached_f2(4) == 8  # Cached, returns "old" value
    assert cached_f2(5) == 10  # Cached, returns "old" value

    Cache("test_parameter").clear()


def test_parameter_dict():
    cached_f = Cache("test_parameter")(lambda x, y: dict(list(x.items()) + list(y.items())))

    assert cached_f({'a': 1, 'b': 2}, {'c': 3}) == {'a': 1, 'b': 2, 'c': 3}
    assert cached_f({'a': 1, 'b': 3}, {'c': 3}) == {'a': 1, 'b': 3, 'c': 3}

    cached_f2 = Cache("test_parameter")(lambda x, y: {})

    assert cached_f2({'a': 1, 'b': 2}, {'c': 3}) == {'a': 1, 'b': 2, 'c': 3}  # Cached, returns "old" value
    assert cached_f2({'a': 1, 'b': 3}, {'c': 3}) == {'a': 1, 'b': 3, 'c': 3}  # Cached, returns "old" value
    assert cached_f2({'a': 2, 'b': 3}, {'c': 3}) == {}  # This one is not cached

    cached_f2.clear()


def test_keyword_args():
    @Cache("keyword")
    def keyword_function(a=1, b=2):
        return a + b

    @Cache("keyword")
    def test_keyword_function(a=1, b=2, c=0):
        return 0

    assert keyword_function() == 3
    assert keyword_function(a=10) == 12
    assert keyword_function(b=10) == 11
    assert keyword_function(b=10, a=10) == 20

    assert test_keyword_function(a=10) == 12
    assert test_keyword_function(b=10) == 11
    assert test_keyword_function(b=10, a=10) == 20
    assert test_keyword_function(a=10, b=10) == 20
    assert test_keyword_function() == 3
    assert test_keyword_function(a=10, b=10, c=1) == 0

    keyword_function.clear()
