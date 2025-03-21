from django.urls import path
from . import views

urlpatterns = [
    path('remittances/', views.remittance_list_view, name='remittance_list'),
    path('remittances/<int:remittance_id>/payments/', views.payment_list_view, name='payment_list'),
]