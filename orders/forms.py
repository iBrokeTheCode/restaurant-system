# forms.py (create if you don't have it)
from django import forms
from django.utils.timezone import now

from menu.models import DailyMenuItem
from orders.models import OrderItem


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('daily_menu_item', 'quantity', 'unit_price', 'note')
        labels = {'note': 'Notes:'}
        widgets = {
            'note': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Notes about order',
                    'style': 'resize: none;',
                    'rows': '3',
                },
            ),
            'unit_price': forms.TextInput(
                attrs={'placeholder': 'Optional (auto filled with default price)'}
            ),
        }

    def __init__(self, *args, **kwargs):
        # Filter daily menu items for today
        super().__init__(*args, **kwargs)
        today = now().date()

        self.fields['daily_menu_item'].queryset = DailyMenuItem.objects.filter(  # type: ignore
            daily_menu__date=today
        )

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('daily_menu_item')
        quantity = cleaned_data.get('quantity')

        if item and quantity:
            # Existing quantity if updating
            existing_quantity = 0
            if self.instance.pk and self.instance.daily_menu_item == item:
                existing_quantity = self.instance.quantity

            # Remaining stock adjusted for this item
            available_stock = item.remaining_stock + existing_quantity

            if quantity > available_stock:
                raise forms.ValidationError(
                    f"Only {available_stock} available for '{item.menu_item.name}'."
                )

        return cleaned_data
