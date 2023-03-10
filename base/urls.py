from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.lead_list),
    path('<int:pk>/', views.lead_detail),
    path('create/', views.lead_create),
]
