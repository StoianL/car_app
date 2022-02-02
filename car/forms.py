from django import forms

from .models import Car, Brand, Repair


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = ('body', 'status', )
