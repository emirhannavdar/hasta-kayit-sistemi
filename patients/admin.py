from django.contrib import admin
from .models import Patient
from .models import Patient, SMSLog

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone_number', 'registration_date',
        'get_notification_date_45_days', 'get_notification_date_60_days'
    )
    search_fields = ('first_name', 'last_name', 'tc_kimlik_no', 'phone_number')
    list_filter = ('registration_date', 'gender')
    readonly_fields = ('registration_date',) # Kayıt tarihi otomatik ayarlandığı için düzenlenemesin

    def get_notification_date_45_days(self, obj):
        return obj.get_notification_date_45_days()
    get_notification_date_45_days.short_description = "45 Gün Sonra Bildirim" # Admin panelinde görünen başlık

    def get_notification_date_60_days(self, obj):
        return obj.get_notification_date_60_days()
    get_notification_date_60_days.short_description = "60 Gün Sonra Bildirim" # Admin panelinde görünen başlık
    
@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('patient', 'message_type', 'status', 'sent_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'message_type', 'status')
    list_filter = ('status', 'message_type')