from django.contrib import admin

from .models import Country, Region, City, Place


class RegionInline(admin.TabularInline):
    model = Region
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    model = Country
    inlines = [RegionInline]


admin.site.register(City)
admin.site.register(Country, CountryAdmin)
admin.site.register(Place)
