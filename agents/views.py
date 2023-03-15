from django.shortcuts import render, reverse
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Agent
from .forms import AgentModelForm


class AgentListView(LoginRequiredMixin, ListView):
    template_name = 'agents/agent_list.html'
    queryset = Agent.objects.all()


class AgentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self) -> str:
        return reverse('agents:agent-list')
    
    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(LoginRequiredMixin, DetailView):
    template_name = 'agents/agent_detail.html'
    queryset = Agent.objects.all()
    context_object_name = 'agent'


class AgentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm
    queryset = Agent.objects.all()

    def get_success_url(self) -> str:
        return reverse('agents:agent-list')


class AgentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'agents/agent_delete.html'
    queryset = Agent.objects.all()

    def get_success_url(self) -> str:
        return reverse('agents:agent-list')

