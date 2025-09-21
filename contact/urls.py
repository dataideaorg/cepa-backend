from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_form, name='contact-form'),
    path('newsletter/', views.newsletter_form, name='newsletter-form'),
    path('contacts/', views.contact_list, name='contact-list'),
    path('newsletters/', views.newsletter_list, name='newsletter-list'),
]
