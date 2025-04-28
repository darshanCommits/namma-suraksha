from django.urls import path
from . import views

app_name = 'legal_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('criminal/', views.criminal_dashboard, name='criminal_dashboard'),
    path('civil/', views.civil_dashboard, name='civil_dashboard'),
    path('family/', views.family_law_dashboard, name='family_law_dashboard'),
    path('property/', views.property_law_dashboard, name='property_law_dashboard'),
    path('consumer/', views.consumer_dashboard, name='consumer_dashboard'),
    path('labour/', views.labour_dashboard, name='labour_dashboard'),
    path('ip/', views.ip_dashboard, name='ip_dashboard'),
    path('public/', views.public_law_dashboard, name='public_law_dashboard'),
    
    # API endpoints
    path('api/case-type-distribution/', views.case_type_distribution_api, name='case_type_distribution_api'),
]

