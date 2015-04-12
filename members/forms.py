from django import forms
from members.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model=Person
        fields= ['name','zipcode', 'streetname', 'housenumber', 'floor', 'door', 'placename', 'email','phone']