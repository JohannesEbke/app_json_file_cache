app\_json\_file\_cache
======================

Provides a function decorator that caches the return value in a JSON file in the appropriate application cache directory.

It requires all function parameters and return values to be encodeable to JSON, so that the cache is human-readable.

It supports a "vary" guard value (e.g. a data model version) that protects against using old versions of cache.

.. image:: https://travis-ci.org/JohannesEbke/app_json_file_cache.svg?branch=master
   :target: https://travis-ci.org/JohannesEbke/app_json_file_cache


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

Caveats
-------

* Names must be unique per app. If you reuse names, chaos ensues.
* Each set of function parameter values creates a new file. This may lead to too many files in a directory on some systems.
* Mixing positional and keyword arguments is not supported
* It's your responsibility that return values are serializable to JSON.
