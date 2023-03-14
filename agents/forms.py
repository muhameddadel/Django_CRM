from django import forms
from base.models import Agent

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('user',)