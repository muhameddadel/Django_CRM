from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead
# Create your views here.

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