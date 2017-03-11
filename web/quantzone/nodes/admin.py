from django.contrib import admin

from .models import *

admin.site.register(Node)
admin.site.register(NodeRelation)

admin.site.register(SubjectTag)