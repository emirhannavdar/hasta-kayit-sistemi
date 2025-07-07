import datetime


def get_notification_date_10_minutes(registration_datetime):
    """Kayıt tarihinden 10 dakika sonrası"""
    return registration_datetime + datetime.timedelta(minutes=10)


def get_notification_date_45_days(registration_datetime):
    """Kayıt tarihinden 45 gün sonrası"""
    return registration_datetime + datetime.timedelta(days=45)


def get_notification_date_60_days(registration_datetime):
    """Kayıt tarihinden 60 gün sonrası"""
    return registration_datetime + datetime.timedelta(days=60)
