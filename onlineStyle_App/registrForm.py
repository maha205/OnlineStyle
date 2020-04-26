from django import forms
from .models import Person

class RegistrForm(forms.ModelForm):
       class Meta:
            model = Person
            fields= ["fullname" ,"email", "mobileno","address", "password" ]
            
       


