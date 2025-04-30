from django import forms

from menu.models import DailyMenu


class DailyMenuForm(forms.ModelForm):
    class Meta:
        model = DailyMenu
        fields = ('date',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
