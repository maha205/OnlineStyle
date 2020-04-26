from django import forms
from .models import Product

class addItemForm(forms.ModelForm):
     #   category = forms.CharField(max_length = 100)

       class Meta:
            model = Product
            fields= ["price","description", "title","qty_small" ,"qty_medium", "qty_large" , "qty_xtraLarge" ,"category"]#,"pic"
           
#"id","price","description", "title","qty_small" ,"qty_medium", "qty_large" , "qty_xtraLarge" ,"category"

            



