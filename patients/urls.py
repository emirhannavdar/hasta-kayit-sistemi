from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, SMSLogListView

router = DefaultRouter()
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sms-logs/', SMSLogListView.as_view(), name='sms_log_list'),
]