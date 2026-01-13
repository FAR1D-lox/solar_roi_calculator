from django import forms
from .models import Region, SolarPanel


class SolarCalculationForm(forms.Form):
    """Форма для ввода данных расчёта окупаемости."""

    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        label="Выберите ваш регион",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="--- Выберите регион ---"
    )

    panel = forms.ModelChoiceField(
        queryset=SolarPanel.objects.all(),
        label="Выберите модель солнечной панели",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="--- Выберите панель ---"
    )

    panel_count = forms.IntegerField(
        label="Количество панелей",
        min_value=1,
        max_value=100,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: 10'
        }),
        help_text="Обычно от 4 до 20 для частного дома"
    )

    monthly_consumption = forms.FloatField(
        label="Ваше среднее потребление электроэнергии (кВт*ч/месяц)",
        min_value=50,
        max_value=5000,
        initial=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: 300'
        }),
        help_text="Обычно от 150 до 800 кВт*ч/месяц для частного дома"
    )

    def clean_panel_count(self):
        """Валидация количества панелей."""
        count = self.cleaned_data['panel_count']
        if count > 50:
            raise forms.ValidationError("Для систем более 50 панелей рекомендуется индивидуальный расчёт.")
        return count

    def clean_monthly_consumption(self):
        """Валидация потребления."""
        consumption = self.cleaned_data['monthly_consumption']
        if consumption < 50:
            raise forms.ValidationError("Потребление слишком низкое для установки солнечной системы.")
        return consumption



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настраиваем стили всех полей
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].help_text = ''  # Убираем стандартные подсказки Django

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user