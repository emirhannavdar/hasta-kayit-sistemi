from celery import shared_task
from django.conf import settings
from twilio.rest import Client
from .models import Patient, SMSLog
from django.utils import timezone
import datetime
from .notification_utils import (
    get_notification_date_45_days,
    get_notification_date_60_days,
    get_notification_date_10_minutes,
)


@shared_task(bind=True)
def send_sms_notification(self, patient_id, message_type):
    """
    Belirli bir hastaya SMS bildirimi gönderen Celery görevi.
    """
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        print(f"Hasta bulunamadı: {patient_id}")
        return

    # Twilio kimlik bilgileri settings.py'den alınır
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    # Twilio istemcisini başlat
    client = Client(account_sid, auth_token)

    # Mesajı türüne göre hazırla
    if message_type == 'welcome':
        message_body = f"Sayın {patient.first_name} {patient.last_name}, kaydınız başarıyla oluşturuldu. Hoş geldiniz! [Klinik Adı]"
        notification_field = None
    elif message_type == '45_day_reminder':
        message_body = f"Sayın {patient.first_name} {patient.last_name}, hasta kaydınızın üzerinden 45 gün geçmiştir. Detaylar için lütfen kliniğimizle iletişime geçin. [Klinik Adı]"
        notification_field = 'last_notification_date_45'
    elif message_type == '60_day_info':
        message_body = f"Sayın {patient.first_name} {patient.last_name}, hasta kaydınızın üzerinden 60 gün geçmiştir. Bilgilendirme için kliniğimizden randevu alabilirsiniz. [Klinik Adı]"
        notification_field = 'last_notification_date_60'
    elif message_type == '10_minutes_info':
        message_body = f"Sayın {patient.first_name} {patient.last_name}, kaydınızın üzerinden 10 dakika geçti. [Klinik Adı]"
        notification_field = 'last_notification_date_10'
    else:
        print(f"Bilinmeyen mesaj tipi: {message_type}")
        return

    try:
        message = client.messages.create(
            to=patient.phone_number,
            from_=twilio_phone_number,
            body=message_body
        )
        print(f"SMS başarıyla gönderildi: {message.sid} - {patient.first_name} {patient.last_name} ({message_type})")

        # SMS log kaydı
        SMSLog.objects.create(
            patient=patient,
            message_type=message_type,
            message_body=message_body,
            status="success"
        )

        # Bildirim gönderildiğinde tarihi güncelle
        if notification_field:
            if notification_field == 'last_notification_date_10':
                setattr(patient, notification_field, timezone.now())
            else:
                setattr(patient, notification_field, timezone.now().date())
            patient.save()

    except Exception as e:
        print(f"SMS gönderilirken hata oluştu: {e} - Hastanın ID'si: {patient.id}")
        SMSLog.objects.create(
            patient=patient,
            message_type=message_type,
            message_body=message_body,
            status="failed",
            error_message=str(e)
        )
        # Hata durumunda tekrar deneme mekanizması (opsiyonel)
        # raise self.retry(exc=e, countdown=60 * 5, max_retries=3)
        # Örneğin, 5 dakika sonra 3 kez daha denemek için yukarıdaki satırı kullanabilirsiniz.


@shared_task
def check_and_send_notifications():
    """
    Tüm hastaları kontrol eder ve gerekli bildirimleri gönderir.
    Bu görev Celery Beat tarafından belirli aralıklarla çalıştırılacak.
    """
    now = timezone.now()
    print(f"Bildirim kontrolü başlatıldı: {now}")

    patients = Patient.objects.all()
    # yeni sayfaya ekle
    for patient in patients:
        # 10 dakikalık bildirim kontrolü
        notification_10_minutes = get_notification_date_10_minutes(patient.registration_date)
        if notification_10_minutes <= now and \
                (patient.last_notification_date_10 is None or patient.last_notification_date_10 < notification_10_minutes):
            print(f"10 dakikalık bildirim: {patient.first_name} {patient.last_name}")
            send_sms_notification.delay(patient.id, '10_minutes_info')

        # 45 günlük bildirim kontrolü
        notification_45_date = get_notification_date_45_days(patient.registration_date)
        if notification_45_date == now.date() and \
                (patient.last_notification_date_45 is None or patient.last_notification_date_45 < now.date()):
            print(f"45 günlük bildirim gönderiliyor: {patient.first_name} {patient.last_name}")
            send_sms_notification.delay(patient.id, '45_day_reminder')

        # 60 günlük bildirim kontrolü
        notification_60_date = get_notification_date_60_days(patient.registration_date)
        if notification_60_date == now.date() and \
                (patient.last_notification_date_60 is None or patient.last_notification_date_60 < now.date()):
            print(f"60 günlük bildirim gönderiliyor: {patient.first_name} {patient.last_name}")
            send_sms_notification.delay(patient.id, '60_day_info')

    print("Bildirim kontrolü tamamlandı.")
