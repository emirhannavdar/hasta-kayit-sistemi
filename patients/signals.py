from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient
from .tasks import send_sms_notification

@receiver(post_save, sender=Patient)
def send_welcome_sms_on_create(sender, instance, created, **kwargs):
    if created:
        send_sms_notification.delay(instance.id, 'welcome') 