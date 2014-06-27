__author__ = 'Craig'

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slowsearch_project.settings")
from django.core.cache import get_cache, cache
import time


cache.set('my_key', 'hello, world!', 5)
print cache.get('my_key')
time.sleep(6)
print cache.get('my_key')



