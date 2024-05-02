# forms.py
from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=100)
    shipping_address = forms.CharField(max_length=100)
    # Add more fields as needed
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CheckoutForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = f'{user.first_name} {user.last_name}'
            self.fields['contact_number'].initial = user.account.contact_number
            self.fields['shipping_address'].initial = user.account.address
            # Pre-populate other fields with user data if needed