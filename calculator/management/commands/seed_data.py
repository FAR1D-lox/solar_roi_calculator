from django.core.management.base import BaseCommand
from calculator.models import SolarPanel, Region
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем заполнение базы тестовыми данными...")

        user, created = User.objects.get_or_create(
            username='testUser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write("Создан тестовый пользователь: testUser / testpass123")

        regions_data = [
            {'name': 'Москва', 'code': 'MOS', 'tariff_day': 6.5, 'tariff_night': 4.2, 'avg_sun_hours': 1700,
             'latitude': 55.7558, 'longitude': 37.6173},
            {'name': 'Санкт-Петербург', 'code': 'SPB', 'tariff_day': 6.2, 'tariff_night': 3.9, 'avg_sun_hours': 1600,
             'latitude': 59.9343, 'longitude': 30.3351},
            {'name': 'Екатеринбург', 'code': 'EKB', 'tariff_day': 4.9, 'tariff_night': 3.1, 'avg_sun_hours': 1650,
             'latitude': 56.8389, 'longitude': 60.6057},
            {'name': 'Сочи', 'code': 'SCH', 'tariff_day': 5.8, 'tariff_night': 3.8, 'avg_sun_hours': 2200,
             'latitude': 43.5855, 'longitude': 39.7231},
            {'name': 'Новосибирск', 'code': 'NSK', 'tariff_day': 5.1, 'tariff_night': 3.3, 'avg_sun_hours': 1800,
             'latitude': 55.0084, 'longitude': 82.9357},
            {'name': 'Краснодар', 'code': 'KRD', 'tariff_day': 5.5, 'tariff_night': 3.5, 'avg_sun_hours': 2100,
             'latitude': 45.0355, 'longitude': 38.9753},
            {'name': 'Казань', 'code': 'KZN', 'tariff_day': 5.3, 'tariff_night': 3.4, 'avg_sun_hours': 1750,
             'latitude': 55.7961, 'longitude': 49.1064},
            {'name': 'Владивосток', 'code': 'VVO', 'tariff_day': 6.0, 'tariff_night': 3.7, 'avg_sun_hours': 2150,
             'latitude': 43.1155, 'longitude': 131.8855},
            {'name': 'Ростов-на-Дону', 'code': 'ROV', 'tariff_day': 5.4, 'tariff_night': 3.4, 'avg_sun_hours': 1900,
             'latitude': 47.2224, 'longitude': 39.7187},
            {'name': 'Нижний Новгород', 'code': 'NNG', 'tariff_day': 5.2, 'tariff_night': 3.3, 'avg_sun_hours': 1680,
             'latitude': 56.3269, 'longitude': 44.0065},
        ]

        regions = []
        for data in regions_data:
            region, created = Region.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            regions.append(region)
            if created:
                self.stdout.write(f"Создан регион: {region.name}")

        panels_data = [
            {'name': 'SunPower X-Series 400W', 'manufacturer': 'SunPower', 'power_w': 400, 'efficiency': 0.22,
             'price': 25000, 'dimensions': '1685×1002×40', 'warranty_years': 25},
            {'name': 'LG NeON R 380W', 'manufacturer': 'LG', 'power_w': 380, 'efficiency': 0.215, 'price': 22000,
             'dimensions': '1700×1016×40', 'warranty_years': 25},
            {'name': 'JA Solar JAM72S30 540W', 'manufacturer': 'JA Solar', 'power_w': 540, 'efficiency': 0.208,
             'price': 18000, 'dimensions': '1722×1134×35', 'warranty_years': 15},
            {'name': 'Canadian Solar HiKu7 670W', 'manufacturer': 'Canadian Solar', 'power_w': 670, 'efficiency': 0.212,
             'price': 21000, 'dimensions': '2384×1303×35', 'warranty_years': 12},
            {'name': 'Trina Solar Vertex S 500W', 'manufacturer': 'Trina Solar', 'power_w': 500, 'efficiency': 0.210,
             'price': 19500, 'dimensions': '1755×1038×35', 'warranty_years': 15},
            {'name': 'REC Alpha Pure 420W', 'manufacturer': 'REC', 'power_w': 420, 'efficiency': 0.218, 'price': 23000,
             'dimensions': '1722×1016×30', 'warranty_years': 20},
            {'name': 'Longi Hi-MO 5 550W', 'manufacturer': 'Longi', 'power_w': 550, 'efficiency': 0.209, 'price': 18500,
             'dimensions': '1722×1134×35', 'warranty_years': 12},
            {'name': 'Jinko Solar Tiger Neo 580W', 'manufacturer': 'Jinko Solar', 'power_w': 580, 'efficiency': 0.224,
             'price': 20500, 'dimensions': '1722×1134×35', 'warranty_years': 15},
            {'name': 'Qcells Q.PEAK DUO BLK 415W', 'manufacturer': 'Qcells', 'power_w': 415, 'efficiency': 0.206,
             'price': 21500, 'dimensions': '2015×1000×30', 'warranty_years': 25},
            {'name': 'Hyundai HiS-S400UI', 'manufacturer': 'Hyundai', 'power_w': 400, 'efficiency': 0.204,
             'price': 17500, 'dimensions': '1685×1002×35', 'warranty_years': 12},
        ]

        panels = []
        for data in panels_data:
            panel, created = SolarPanel.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            panels.append(panel)
            if created:
                self.stdout.write(f"Создана панель: {panel.name}")

        self.stdout.write(self.style.SUCCESS(f"Успешно создано: {len(regions)} регионов, {len(panels)} панелей"))
        self.stdout.write("Админка доступна по адресу: http://127.0.0.1:8000/admin или localhost:8000/admin")
        self.stdout.write("Логин: Imperator / Пароль: неправильный пароль")