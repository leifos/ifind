__author__ = 'leif'

from django.contrib import admin
from calibrate.models import TestCollection, Topic, Document

# updates to admin

admin.site.register(TestCollection)
admin.site.register(Topic)
admin.site.register(Document)