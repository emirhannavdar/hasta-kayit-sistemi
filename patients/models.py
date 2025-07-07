from django.db import models
from django.utils import timezone
import datetime

class Patient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    date_of_birth = models.DateField(verbose_name="Doğum Tarihi", null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Erkek'), ('F', 'Kadın'), ('O', 'Diğer')],
        verbose_name="Cinsiyet",
        null=True,
        blank=True
    )
    tc_kimlik_no = models.CharField(max_length=11, unique=True, verbose_name="TC Kimlik Numarası", null=True, blank=True)

    # İletişim Bilgileri
    phone_number = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    email = models.EmailField(verbose_name="E-posta", null=True, blank=True)
    address = models.TextField(verbose_name="Adres", null=True, blank=True)

    # Tıbbi Bilgiler
    medical_history = models.TextField(verbose_name="Tıbbi Geçmiş", null=True, blank=True)
    allergies = models.TextField(verbose_name="Alerjiler", null=True, blank=True)
    current_medications = models.TextField(verbose_name="Mevcut İlaçlar", null=True, blank=True)

    # Kayıt Bilgileri
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="Kayıt Tarihi")
    last_notification_date_45 = models.DateField(verbose_name="Son 45 Gün Bildirim Tarihi", null=True, blank=True)
    last_notification_date_60 = models.DateField(verbose_name="Son 60 Gün Bildirim Tarihi", null=True, blank=True)
    last_notification_date_10 = models.DateTimeField(verbose_name="Son 10 Dakika Bildirim Tarihi", null=True, blank=True)

    class Meta:
        verbose_name = "Hasta"
        verbose_name_plural = "Hastalar"
        ordering = ['-registration_date'] # Kayıt tarihine göre tersten sırala

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.tc_kimlik_no or 'TC No Yok'})"

    def get_notification_date_45_days(self):
        """Kayıt tarihinden 45 gün sonra"""
        return self.registration_date + datetime.timedelta(days=45)

    def get_notification_date_60_days(self):
        """Kayıt tarihinden 60 gün sonra"""
        return self.registration_date + datetime.timedelta(days=60)
    
    def get_notification_date_10_minutes(self):
        """Kayıt tarihinden 10 dakika sonra"""
        return self.registration_date + datetime.timedelta(minutes=10)
    

class SMSLog(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="sms_logs")
    message_type = models.CharField(max_length=50)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="success")  # success, failed, vs.
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient} - {self.message_type} - {self.sent_at}"
    