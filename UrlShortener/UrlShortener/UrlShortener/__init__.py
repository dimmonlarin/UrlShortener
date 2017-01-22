"""
The flask application package.
"""

from flask import Flask
from flask_cache import Cache
app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
import UrlShortener.views, UrlShortener.api
