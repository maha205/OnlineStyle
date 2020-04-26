from django import forms

class EditFreeShippingForm(forms.Form):
   priceShipping = forms.CharField(max_length = 100)
   priceAmonut = forms.CharField(max_length = 100)

