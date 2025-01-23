app\_json\_file\_cache
======================

Provides a function decorator that caches the return value in a JSON file in the appropriate application cache directory.

It requires all function parameters and return values to be encodeable to JSON, so that the cache content
is human-readable. The file names are based on a SHA512 hash of the function parameters.

It supports a "vary" guard value (e.g. a data model version) that protects against using old versions of cache.

Additionally, a cheaper default function (e.g. returning shipped, precalculated values) can be specified as a stand-in
until an explicit recalculate function is called.

.. image:: https://img.shields.io/pypi/v/app-json-file-cache
   :alt: PyPI
   :target: https://pypi.org/project/app-json-file-cache/

.. image:: https://github.com/JohannesEbke/app_json_file_cache/actions/workflows/test.yaml/badge.svg
   :target: https://github.com/JohannesEbke/app_json_file_cache/actions/workflows/test.yaml/


Usage
-----

Example usage::

  from app_json_file_cache import AppCache
  cache = AppCache("myapp")

  @cache("expensive")
  def expensive_function():
      return calculator()

More Example usage::

  from app_json_file_cache import AppCache
  cache = AppCache("myapp")

  @cache("expensive", vary=VERSION)
  def expensive_function(param):
      return calculator(param)

  expensive_function.recalculate(param1) # recalculate if external effects change

Using a default function until the next recalculate::

  from app_json_file_cache import AppCache
  cache = AppCache("myapp")

  def cheap_standin(param):
      return estimate(param)

  @cache("expensive", vary=VERSION, cheap_default_func=cheap_standin)
  def expensive_function(param):
      return calculator(param)

  expensive_function(param1) # cheap_standin is used
  expensive_function.recalculate(param1) # cache is updated with expensive_function
  expensive_function(param1) # cached value from expensive_function is used

Caveats
-------

* Names must be unique per app. If you reuse names, chaos ensues.
* Each set of function parameter values creates a new file. This may lead to too many files in a directory on some systems.
* Mixing positional and keyword arguments is not supported
* It's your responsibility that return values are serializable to JSON.
