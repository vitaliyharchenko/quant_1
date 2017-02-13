from django.contrib import admin

from .models import *


class RegionInline(admin.TabularInline):
    model = Region
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    model = Country
    inlines = [RegionInline]


admin.site.register(City)
admin.site.register(Country, CountryAdmin)
admin.site.register(Place)
admin.site.register(Office)
admin.site.register(СlassRoom)
