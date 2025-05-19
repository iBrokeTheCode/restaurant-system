from django import forms

from menu.models import DailyMenu, MenuItem


class DailyMenuForm(forms.ModelForm):
    class Meta:
        model = DailyMenu
        fields = ('date',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'price', 'category', 'image')
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'style': 'resize: none;'}
            )
        }
