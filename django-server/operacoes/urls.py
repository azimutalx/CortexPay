from django.urls import path
from . import views

urlpatterns = [
    path('remittances/', views.remittance_list_view, name='remittance_list'),
    path('remittances/<int:remittance_id>/payments/', views.payment_list_view, name='payment_list'),
    path('remittances/create/', views.remittance_create_view, name='remittance_create'),
    path('remittances/<int:remittance_id>/edit/', views.remittance_edit_view, name='remittance_edit'),
    path('payments/<int:payment_id>/edit/', views.payment_edit_view, name='payment_edit'),
]