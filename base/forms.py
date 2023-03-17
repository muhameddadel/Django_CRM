from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent

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


class AssignAgentFrom(forms.Form):
    agent = forms.ModelChoiceField(queryset= Agent.objects.none())

    def __init(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organisation = request.user.userprofile)
        super(AssignAgentFrom, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents