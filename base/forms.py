from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'

class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    age = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username',)
        field_classes = {'username': UsernameField}