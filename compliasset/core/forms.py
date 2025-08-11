from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Asset

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'location', 'model_number', 'serial_number', 'purchase_date', 'warranty_document']