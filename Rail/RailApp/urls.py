from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('admins/',views.admin,name='admin'),
    path('classified/', views.classified, name='classified'),
    path('complaint/', views.file_complaint, name='complaint'),
    path('track/', views.track_complaint, name='track'),
    path('analytics/', views.analytics, name='analytics'),
    path('help/', views.help_support, name='help'),
    path('resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path('delete_complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),

]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

