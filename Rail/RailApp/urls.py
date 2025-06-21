from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('complaint/', views.file_complaint, name='complaint'),
    path('track/', views.track_complaint, name='track'),
    path('analytics/', views.analytics, name='analytics'),
    path('help/', views.help_support, name='help'),
]
