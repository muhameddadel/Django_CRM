from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import *
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import *
from .forms import *
# Create your views here.

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')

    
class LandingPageView(TemplateView):
    template_name = 'landing.html'
    

class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'base/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull= False)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation, agent__isnull= False)
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



class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    form_class = LeadModelForm
    template_name = 'base/lead_create.html'
    
    def get_success_url(self) -> str:
        return reverse('base:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject='A lead has been created',
            message='Go to the site to see the new lead',
            from_email='test@test.com',
            recipient_list=['test@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    form_class = LeadModelForm
    template_name = 'base/lead_update.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)
    
    def get_success_url(self) -> str:
        return reverse('base:lead-list')


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'base/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)

    def get_success_url(self) -> str:
        return reverse('base:lead-list')


class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = 'base/assign_agent.html'
    form_class = AssignAgentFrom

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse('base:lead-list')
    
    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id = self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'base/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context= super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation= user.agent.organisation)
        
        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull= True).count()
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation= user.agent.organisation)
        return queryset
    

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'base/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation= user.agent.organisation)
        return queryset
    

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'base/lead_category_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation= user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation= user.agent.organisation)
            queryset = queryset.filter(agent__user= user)
        return queryset
    
    def get_success_url(self) -> str:
        return reverse('base:lead-detail', kwargs = {'pk': self.get_object().id})
