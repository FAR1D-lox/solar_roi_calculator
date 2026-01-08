from django.contrib import admin
from .models import SolarPanel, Region, Calculation

@admin.register(SolarPanel)
class SolarPanelAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'power_w', 'efficiency', 'price', 'warranty_years']
    list_filter = ['manufacturer', 'warranty_years']
    search_fields = ['name', 'manufacturer']
    ordering = ['-price']
    list_per_page = 20

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'tariff_day', 'tariff_night', 'avg_sun_hours']
    list_filter = ['tariff_day']
    search_fields = ['name', 'code']
    ordering = ['name']
    list_per_page = 20

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'region', 'panel', 'panel_count', 'total_cost', 'payback_years', 'created_at']
    list_filter = ['region', 'created_at']
    search_fields = ['user__username', 'region__name', 'panel__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ('Параметры расчета', {
            'fields': ('user', 'region', 'panel', 'panel_count', 'monthly_consumption')
        }),
        ('Результаты', {
            'fields': ('total_cost', 'system_power_kw', 'yearly_production_kwh',
                       'yearly_saving', 'payback_years', 'co2_saved_kg')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        })
    )