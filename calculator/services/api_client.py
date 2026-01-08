class EnergyDataClient:
    """Клиент для получения данных из внешних API (согласно ТЗ: NASA POWER API, Mock API поставщиков)."""

    def get_tariffs_by_region(self, region_code):
        """Получает тарифы на электроэнергию по коду региона (Mock API поставщиков)."""
        # Имитируем запрос к API.
        print(f"[API] Запрос тарифов для региона: {region_code}")

        mock_tariffs = {
            'MOS': {'day': 6.5, 'night': 4.2, 'updated': '2024-01-01'},
            'SPB': {'day': 6.2, 'night': 3.9, 'updated': '2024-01-01'},
            'EKB': {'day': 4.9, 'night': 3.1, 'updated': '2024-01-01'},
            'SCH': {'day': 5.8, 'night': 3.8, 'updated': '2024-01-01'},
            'NSK': {'day': 5.1, 'night': 3.3, 'updated': '2024-01-01'},
            'KRD': {'day': 5.5, 'night': 3.5, 'updated': '2024-01-01'},
            'KZN': {'day': 5.3, 'night': 3.4, 'updated': '2024-01-01'},
            'VVO': {'day': 6.0, 'night': 3.7, 'updated': '2024-01-01'},
            'ROV': {'day': 5.4, 'night': 3.4, 'updated': '2024-01-01'},
            'NNG': {'day': 5.2, 'night': 3.3, 'updated': '2024-01-01'},
        }
        return mock_tariffs.get(region_code, {'day': 5.5, 'night': 3.5, 'updated': '2024-01-01'})

    def get_solar_irradiance(self, latitude, longitude):
        """Получает данные по солнечной инсоляции (ТЗ: NASA POWER API)."""
        # Имитируем структуру запроса к реальному API NASA
        params = {
            'parameters': 'ALLSKY_SFC_SW_DWN',
            'community': 'RE',
            'longitude': longitude,
            'latitude': latitude,
            'start': '20240101',
            'end': '20241231',
            'format': 'JSON',
        }
        print(f"[API] Запрос солнечной инсоляции для координат: ({latitude}, {longitude})")

        try:
            # Потом сделаю так:
            # response = requests.get('https://power.larc.nasa.gov/api/temporal/daily/point', params=params)
            # data = response.json()
            # ... обработка сложного JSON от NASA ...

            # Упрощенная формула: базовые часы + поправка на широту
            base_hours = 1700
            lat_factor = abs(latitude) / 90  # от 0 до 1
            adjusted_hours = int(base_hours * (1 - lat_factor * 0.3))  # уменьшаем к полюсам

            return {
                'annual_sun_hours': adjusted_hours,
                'source': 'NASA POWER API (mock)',
                'latitude': latitude,
                'longitude': longitude
            }
        except Exception:
            # Среднее значение в случае "ошибки" API
            return {'annual_sun_hours': 1700, 'source': 'fallback data'}