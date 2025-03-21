from django.urls import path
from . import views

urlpatterns = [
    path('remittances/', views.remittance_list_view, name='remittance_list'),
]