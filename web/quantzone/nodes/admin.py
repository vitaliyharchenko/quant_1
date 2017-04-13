from django.contrib import admin

from .models import *
from .autocomplete import NodeRelationForm


class NodeRelationAdmin(admin.ModelAdmin):
    form = NodeRelationForm


admin.site.register(Node)
admin.site.register(NodeRelation, NodeRelationAdmin)
admin.site.register(SubjectTag)
