from django import forms
class EditSaleForm(forms.Form):
   discount = forms.CharField(max_length = 100)

