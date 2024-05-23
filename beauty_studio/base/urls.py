from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services', views.services, name='services'),
    path('order', views.order, name='order'),
    path('gallery', views.gallery, name='gallery'),
    path('partnership', views.partnership, name='partnership'),
    path('completeForm', views.completeForm, name='completeForm'),
    path('add_to_chosen_services/', views.add_to_chosen_services, name='add_to_chosen_services'),
    path('delete_from_chosen_services/', views.delete_from_chosen_services, name='delete_from_chosen_services'),
]
