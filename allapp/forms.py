from django import forms
from .models import CustomUser
from .models import Medicine 
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from PIL import Image  
from .models import DoctorAdditionalDetails
from .models import Doctor
from .models import Testimonial




# patient details
class PatientProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'dob']  # Include 'dob' in the fields list
        

# class DoctorDetailsForm(forms.ModelForm):
#     class Meta:
#         model = DoctorAdditionalDetails
#         fields = ['picture', 'registration_number', 'experience', 'specialty', 'education']


class DoctorAdditionalDetailsForm(forms.ModelForm):
    class Meta:
        model = DoctorAdditionalDetails
        fields = ['picture', 'registration_number', 'experience', 'specialty', 'education']
        
        
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

    def clean_med_image(self):
        image = self.cleaned_data.get('med_image')
        max_image_size = 5 * 1024 * 1024  # 5 MB (adjust as needed)
        max_width = 200  # Adjust the maximum width as needed
        max_height = 300 # Adjust the maximum height as needed

        if image:
            if image.size > max_image_size:
                raise ValidationError("Image size should be less than 5MB.")
            
            img = Image.open(image)
            width, height = img.size

            if width > max_width or height > max_height:
                raise ValidationError(f"Image dimensions should not exceed {max_width}x{max_height} pixels.")
            
        return image


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'dob']

class DoctorAdditionalDetailsForm(forms.ModelForm):
    class Meta:
        model = DoctorAdditionalDetails
        fields = ['picture', 'registration_number', 'experience', 'specialty', 'education']


from django.views.generic.list import ListView
class AllDoctorsListView(ListView):
    template_name = 'all_doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        # Fetch all doctors and their additional details
        doctors = Doctor.objects.all()
        details = DoctorAdditionalDetails.objects.all()
        
        # Combine the data into a list of tuples (doctor, additional_details)
        doctor_data = []
        for doctor in doctors:
            additional_details = details.filter(doctor=doctor).first()
            doctor_data.append((doctor, additional_details))

        return doctor_data
    
   
from .models import ConsultationRequest
class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['image', 'description']


class ConsultationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2)
    appointment_needed = forms.BooleanField(required=False)
    
    
# appointment
from .models import Appointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot', 'patient_name', 'patient_email']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['rating', 'feedback']
        

from .models import Clinic
#clinic works
# class ClinicForm(forms.ModelForm):
#     class Meta:
#         model = Clinic
#         fields = ['clinic_name', 'contact_number', 'email', 'speciality', 'location', 'image']

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['clinic_name', 'contact_number', 'email', 'speciality', 'location', 'image', 'doctors']

    def __init__(self, *args, **kwargs):
        super(ClinicForm, self).__init__(*args, **kwargs)
        self.fields['doctors'].widget = forms.CheckboxSelectMultiple()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot']
