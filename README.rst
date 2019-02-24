xdg\_json\_cache
================

Provides a function decorator that caches the return value in a JSON file in the appropriate XDG cache directory.

 * Currently no support for function parameters. Only one value per cache.
 * Support for dropping the cache if a "vary" value changed, e.g. your program version.

Usage
-----

Example usage::

  from xdg_json_cache import make_app_cache
  Cache = make_app_cache("myapp")

  @Cache("expensive")
  def expensive_function():
      return calculator()

More Example usage::

  from xdg_json_cache import make_app_cache
  Cache = make_app_cache("myapp")

  @Cache("expensive", vary=VERSION)
  def expensive_function():
      return calculator()

Caveats
-------

 * Names must be unique per app. If you reuse names, chaos ensues.
 * It's your responsibility that return values are serializable to JSON.
