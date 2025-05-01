# forms.py (create if you don't have it)
from django import forms

from orders.models import OrderItem


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('daily_menu_item', 'quantity', 'unit_price', 'note')

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('daily_menu_item')
        quantity = cleaned_data.get('quantity')

        if item and quantity:
            # Check remaining stock
            if quantity > item.remaining_stock:
                raise forms.ValidationError(
                    f"Only {item.remaining_stock} available for '{item.menu_item.name}'."
                )

        return cleaned_data
