from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import *
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
# Create your views here.

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')

class LandingPageView(TemplateView):
    template_name = 'landing.html'


def landing_page(request):
    return render(request, 'landing.html')


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'base/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull = True)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation, agent__isnull = True)
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull = True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request,'base/lead_list.html', context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'base/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            queryset = queryset.filter(agent__user = user)
        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(pk= pk)
    context = {
        'lead': lead
    }
    return render(request, 'base/lead_detail.html', context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    form_class = LeadModelForm
    template_name = 'base/lead_create.html'
    
    def get_success_url(self) -> str:
        return reverse('base:lead-list')

    def form_valid(self, form):
        send_mail(
            subject='A lead has been created',
            message='Go to the site to see the new lead',
            from_email='test@test.com',
            recipient_list=['test@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/base')
    else:
        form = LeadModelForm()

    context = {
        "form": form
    }
    return render(request, 'base/lead_create.html', context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    form_class = LeadModelForm
    template_name = 'base/lead_update.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)
    
    def get_success_url(self) -> str:
        return reverse('base:lead-list')


def lead_update(request, pk):
    lead = Lead.objects.get(pk= pk)
    form = LeadModelForm(instance= lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance= lead)
        if form.is_valid():
            form.save()
            return redirect('/base')
    context = {
        'form': form,
        'lead': lead
    }
    return render(request, 'base/lead_update.html', context)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'base/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)

    def get_success_url(self) -> str:
        return reverse('base:lead-list')

def lead_delete(request, pk):
    lead = Lead.objects.get(pk = pk)
    lead.delete()
    return redirect('/base')