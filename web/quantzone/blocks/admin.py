from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import Block, TextBlock, ChoiceBlock


# Register your models here.
admin.site.register(Block)
admin.site.register(TextBlock, MarkdownxModelAdmin)
admin.site.register(ChoiceBlock)
