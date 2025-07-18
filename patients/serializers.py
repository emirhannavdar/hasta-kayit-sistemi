from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__' # Modeldeki tüm alanları API'de göster
        read_only_fields = ('registration_date',) # Sadece okunabilir, API üzerinden değiştirilemez