# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Django'nun yerleşik auth görünümleri için
from patients.views import home_view, patient_list_view, add_patient_view, edit_patient_view, delete_patient_view, SMSLogListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('patients.urls')), # patients uygulamasının API URL'leri (önceden vardı)
    path('api-auth/', include('rest_framework.urls')), # REST Framework kimlik doğrulama URL'leri (önceden vardı)

    # Web Sayfası URL'leri
    path('', home_view, name='home'),
    path('patients/', patient_list_view, name='patient_list'),
    path('patients/add/', add_patient_view, name='add_patient'),
    path('patients/edit/<int:pk>/', edit_patient_view, name='edit_patient'),
    path('patients/delete/<int:pk>/', delete_patient_view, name='delete_patient'),
    path('sms-logs/', SMSLogListView.as_view(), name='sms_log_list'),

    # Kimlik Doğrulama URL'leri
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]