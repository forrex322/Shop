from django import forms

from .models import Order

class OrderForm(forms.ModelForm):

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Data when order was geted'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            "first_name", "last_name", "phone", "address", "baying_type", "order_date", "comment"
        )