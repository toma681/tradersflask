from flask_caching import Cache
#cache = Cache(config={"CACHE_TYPE": "FileSystemCache", "CACHE_DIR": "./cache", "CACHE_DEFAULT_TIMEOUT": 10000})
cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 10000})
