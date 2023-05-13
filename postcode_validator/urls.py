from django.urls import path
from . import views

urlpatterns = [
    path('validate_postcode/', views.validate_postcode, name='validate_postcode'),
    path('format_postcode/', views.format_postcode, name='format_postcode'),
]

