from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import TextBlock, ChoiceBlock, ChoiceBlockOption


class ChoiceBlockOptionInline(admin.TabularInline):
    model = ChoiceBlockOption
    extra = 4


class ChoiceBlockAdmin(admin.ModelAdmin):
    inlines = [ChoiceBlockOptionInline]


# Register your models here.
admin.site.register(TextBlock, MarkdownxModelAdmin)
admin.site.register(ChoiceBlock, ChoiceBlockAdmin)
