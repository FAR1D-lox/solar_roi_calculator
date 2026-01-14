import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class SolarROICalculator:
    """Основной калькулятор окупаемости."""

    def __init__(self, panel, panel_count, region, monthly_consumption):
        self.panel = panel
        self.panel_count = panel_count
        self.region = region
        self.monthly_consumption = monthly_consumption

        from .api_client import EnergyDataClient
        self.api_client = EnergyDataClient()

    def calculate(self):
        """Основной метод расчета. Возвращает словарь с результатами и графиком."""

        total_power_w = self.panel.power_w * self.panel_count
        total_power_kw = total_power_w / 1000

        from .api_client import EnergyDataClient
        api_client = EnergyDataClient()

        # Данные по солнечной инсоляции из NASA API
        solar_data = api_client.get_solar_irradiance(
            latitude=self.region.latitude,
            longitude=self.region.longitude
        )

        real_sun_hours = solar_data['annual_sun_hours']

        data_source = solar_data.get('source', 'unknown')
        print(f"[SolarCalculator] Используем {real_sun_hours} солнечных часов/год (источник: {data_source})")

        # Годовая выработка системы (кВт·ч)
        yearly_production_kwh = total_power_kw * real_sun_hours * self.panel.efficiency

        # Годовое потребление дома (кВт·ч)
        yearly_consumption_kwh = self.monthly_consumption * 12

        # ЭФФЕКТИВНАЯ выработка (не может превышать потребление)
        effective_production_kwh = min(yearly_production_kwh, yearly_consumption_kwh)

        # Процент покрытия потребления
        coverage_percentage = (
                    effective_production_kwh / yearly_consumption_kwh * 100) if yearly_consumption_kwh > 0 else 0

        # Экономия ТОЛЬКО от использованной энергии
        yearly_saving = effective_production_kwh * float(self.region.tariff_day)

        # Стоимость системы
        system_cost = float(self.panel.price) * self.panel_count * 1.3

        # Срок окупаемости
        payback_years = system_cost / yearly_saving if yearly_saving > 0 else 0

        # Излишки производства (если есть)
        excess_production_kwh = max(0, yearly_production_kwh - yearly_consumption_kwh)

        df_data = {
            'Параметр': ['Мощность системы', 'Годовая выработка', 'Годовая экономия', 'Срок окупаемости'],
            'Значение': [
                f"{round(total_power_kw, 2)} кВт",
                f"{round(yearly_production_kwh, 0)} кВт*ч",
                f"{round(yearly_saving, 2)} руб.",
                f"{round(payback_years, 1)} лет"
            ],
            'Единица измерения': ['кВт', 'кВт*ч', 'руб.', 'лет']
        }
        results_df = pd.DataFrame(df_data)

        roi_chart_base64 = self._generate_roi_chart(system_cost, yearly_saving, payback_years)

        return {
            'total_cost': round(system_cost, 2),
            'system_power_kw': round(total_power_kw, 2),
            'yearly_production_kwh': round(yearly_production_kwh, 0),
            'yearly_saving': round(yearly_saving, 2),
            'payback_years': round(payback_years, 1),
            'co2_saved_kg': round(yearly_production_kwh * 0.5, 0),  # упрощенный расчет CO2
            'calculation_df': results_df,
            'roi_chart': roi_chart_base64,
            'yearly_consumption_kwh': round(yearly_consumption_kwh, 0),
            'effective_production_kwh': round(effective_production_kwh, 0),
            'coverage_percentage': round(coverage_percentage, 1),
            'excess_production_kwh': round(excess_production_kwh, 0),
            'is_overproduction': yearly_production_kwh > yearly_consumption_kwh,
            'solar_data_source': data_source,
            'real_sun_hours': real_sun_hours,
        }

    def _generate_roi_chart(self, system_cost, yearly_saving, payback_years):
        """Генерирует график окупаемости и возвращает его в виде строки base64."""
        # Данные для 15 лет или до окупаемости + 5 лет
        max_years = max(15, int(payback_years) + 5)
        years = list(range(0, max_years + 1))

        # Накопленная экономия по годам
        cumulative_savings = [0]
        for year in years[1:]:
            cumulative_savings.append(yearly_saving * year)

        # Построение графика
        plt.figure(figsize=(10, 6))
        plt.plot(years, cumulative_savings, 'b-', linewidth=2, label='Накопленная экономия')
        plt.axhline(y=system_cost, color='r', linestyle='--', label=f'Стоимость системы ({system_cost:,.0f} руб.)')

        # Вертикальная линия окупаемости, если она в пределах графика
        if payback_years <= max_years:
            plt.axvline(x=payback_years, color='g', linestyle=':', label=f'Окупаемость ({payback_years:.1f} лет)')

        plt.fill_between(years, cumulative_savings, system_cost,
                         where=[s <= system_cost for s in cumulative_savings],
                         alpha=0.2, color='orange', label='Период окупаемости')

        plt.title('График окупаемости солнечной электростанции', fontsize=14)
        plt.xlabel('Годы', fontsize=12)
        plt.ylabel('Рубли', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()

        # Конвертация графика в base64 для вставки в HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()

        return base64.b64encode(image_png).decode('utf-8')