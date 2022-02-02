from django.contrib import admin

from .models import Car, Brand, Repair

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('reg_num', 'vin_num', 'brand')
    search_fields = ('reg_num', 'vin_num')

@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('body', 'car', 'status')
    search_fields = ('body', )
    list_filter = ('status', 'created', 'updated')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fileds = ('name', )
