from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from .forms import SolarCalculationForm
from .models import Calculation, SolarPanel, Region
from .services.calculator import SolarROICalculator


def home(request):
    """Главная страница со статистикой."""
    total_calculations = Calculation.objects.count()
    avg_payback = Calculation.objects.aggregate(Avg('payback_years'))
    total_co2_saved = Calculation.objects.aggregate(Sum('co2_saved_kg'))

    # Самые популярные панели
    popular_panels = SolarPanel.objects.annotate(
        calc_count=Count('calculation')
    ).order_by('-calc_count')[:5]

    context = {
        'total_calculations': total_calculations,
        'avg_payback': round(avg_payback['payback_years__avg'] or 0, 1),
        'total_co2_saved': total_co2_saved['co2_saved_kg__sum'] or 0,
        'popular_panels': popular_panels,
        'title': 'Solar ROI Calculator'
    }
    return render(request, 'calculator/home.html', context)


def calculate(request):
    """Страница расчёта окупаемости."""
    result = None

    if request.method == 'POST':
        form = SolarCalculationForm(request.POST)
        if form.is_valid():
            region = form.cleaned_data['region']
            panel = form.cleaned_data['panel']
            panel_count = form.cleaned_data['panel_count']
            monthly_consumption = form.cleaned_data['monthly_consumption']

            calculator = SolarROICalculator(
                panel=panel,
                panel_count=panel_count,
                region=region,
                monthly_consumption=monthly_consumption
            )

            result = calculator.calculate()

            if request.user.is_authenticated:
                calculation = Calculation.objects.create(
                    user=request.user,
                    region=region,
                    panel=panel,
                    panel_count=panel_count,
                    monthly_consumption=monthly_consumption,
                    total_cost=result['total_cost'],
                    system_power_kw=result['system_power_kw'],
                    yearly_production_kwh=result['yearly_production_kwh'],
                    yearly_saving=result['yearly_saving'],
                    payback_years=result['payback_years'],
                    co2_saved_kg=result['co2_saved_kg']
                )
                messages.success(request, 'Ваш расчёт сохранён в истории!')

            # Передаю форму снова, чтобы показать её с заполненными данными
            context = {
                'form': form,
                'result': result,
                'title': 'Результаты расчёта'
            }
            return render(request, 'calculator/calculate.html', context)
    else:
        form = SolarCalculationForm()

    context = {
        'form': form,
        'title': 'Калькулятор окупаемости'
    }
    return render(request, 'calculator/calculate.html', context)


@login_required
def history(request):
    """История расчётов для авторизованных пользователей."""
    calculations = Calculation.objects.filter(user=request.user).order_by('-created_at')

    # Агрегация по истории (сложный ORM-запрос)
    stats = calculations.aggregate(
        total_investment=Sum('total_cost'),
        total_saving_per_year=Sum('yearly_saving'),
        avg_payback=Avg('payback_years')
    )

    context = {
        'calculations': calculations,
        'stats': stats,
        'title': 'История расчётов'
    }
    return render(request, 'calculator/history.html', context)