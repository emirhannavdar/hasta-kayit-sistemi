from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Mesajları göstermek için
from .models import Patient, SMSLog
from .forms import PatientForm # Formu henüz oluşturmadık, bir sonraki adımda yapacağız

# API Görünümleri (Mevcut haliyle kalsın)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientSerializer

from django.views.generic import ListView

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class SMSLogListView(ListView):
    model = SMSLog
    template_name = "patients/sms_log_list.html"
    context_object_name = "logs"
    paginate_by = 25

# --- Web Sayfası Görünümleri ---

@login_required
def home_view(request):
    """Ana sayfa görünümü."""
    return render(request, 'home.html')

@login_required
def patient_list_view(request):
    """Tüm hastaları listeleyen görünüm."""
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

@login_required
def add_patient_view(request):
    """Yeni hasta ekleme görünümü."""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hasta başarıyla eklendi!')
            return redirect('patient_list')
        else:
            messages.error(request, 'Hasta eklenirken bir hata oluştu. Lütfen formu kontrol edin.')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

@login_required
def edit_patient_view(request, pk):
    """Mevcut hasta bilgilerini düzenleme görünümü."""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hasta bilgileri başarıyla güncellendi!')
            return redirect('patient_list')
        else:
            messages.error(request, 'Hasta bilgileri güncellenirken bir hata oluştu. Lütfen formu kontrol edin.')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

@login_required
def delete_patient_view(request, pk):
    """Hasta silme görünümü."""
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Hasta başarıyla silindi!')
        return redirect('patient_list')
    return render(request, 'confirm_delete.html', {'patient': patient})