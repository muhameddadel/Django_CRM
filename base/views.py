from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import *
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm
# Create your views here.


class LandingPageView(TemplateView):
    template_name = 'landing.html'


def landing_page(request):
    return render(request, 'landing.html')


class LeadListView(ListView):
    queryset = Lead.objects.all()
    template_name = 'base/lead_list.html'
    context_object_name = 'leads'


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request,'base/lead_list.html', context)


class LeadDetailView(DetailView):
    queryset = Lead.objects.all()
    template_name = 'base/lead_detail.html'
    context_object_name = 'lead'


def lead_detail(request, pk):
    lead = Lead.objects.get(pk= pk)
    context = {
        'lead': lead
    }
    return render(request, 'base/lead_detail.html', context)


class LeadCreateView(CreateView):
    form_class = LeadModelForm
    template_name = 'base/lead_create.html'
    
    def get_success_url(self) -> str:
        return reverse('base:lead-list')


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


class LeadUpdateView(UpdateView):
    form_class = LeadModelForm
    queryset = Lead.objects.all()
    template_name = 'base/lead_update.html'
    
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


class LeadDeleteView(DeleteView):
    queryset = Lead.objects.all()
    template_name = 'base/lead_delete.html'

    def get_success_url(self) -> str:
        return reverse('base:lead-list')

def lead_delete(request, pk):
    lead = Lead.objects.get(pk = pk)
    lead.delete()
    return redirect('/base')