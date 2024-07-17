from django.contrib import admin

from pottery.organization.models import City, Filiation, Street


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    pass


@admin.register(Filiation)
class FiliationAdmin(admin.ModelAdmin):
    pass
