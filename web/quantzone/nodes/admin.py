from django.contrib import admin

from nodes.models import *

admin.site.register(Node)
admin.site.register(NodeRelation)
admin.site.register(SubjectTag)
