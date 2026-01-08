from django.db import models
from django.contrib.auth.models import User


class SolarPanel(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=100)
    power_w = models.IntegerField(verbose_name="Мощность (Вт)")
    efficiency = models.FloatField(verbose_name="КПД")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=50, help_text="ШхВхТ в мм", blank=True)
    warranty_years = models.IntegerField(default=25)

    def __str__(self):
        return f"{self.name} ({self.power_w}W)"


class Region(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    tariff_day = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Тариф день (руб/кВтч)")
    tariff_night = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Тариф ночь")
    avg_sun_hours = models.FloatField(verbose_name="Солнечные часы в год")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    panel = models.ForeignKey(SolarPanel, on_delete=models.CASCADE)
    panel_count = models.IntegerField(default=10)
    monthly_consumption = models.FloatField(verbose_name="Потребление (кВтч/мес)")

    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    system_power_kw = models.FloatField(verbose_name="Мощность системы (кВт)", blank=True, null=True)
    yearly_production_kwh = models.FloatField(verbose_name="Выработка (кВтч/год)", blank=True, null=True)
    yearly_saving = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payback_years = models.FloatField(blank=True, null=True)
    co2_saved_kg = models.FloatField(verbose_name="Сэкономлено CO2 (кг/год)", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Расчет"
        verbose_name_plural = "Расчеты"

    def __str__(self):
        return f"Расчет от {self.created_at.strftime('%d.%m.%Y')}"