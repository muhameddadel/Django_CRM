from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm
# Create your views here.


def landing_page(request):
    return render(request, 'landing.html')


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request,'base/lead_list.html', context)


def lead_detail(request, pk):
    lead = Lead.objects.get(pk= pk)
    context = {
        'lead': lead
    }
    return render(request, 'base/lead_detail.html', context)


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


def lead_delete(request, pk):
    lead = Lead.objects.get(pk = pk)
    lead.delete()
    return redirect('/base')