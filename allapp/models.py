from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None,dob=None, **extra_fields):     #, role='Patient'
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email,dob=dob, **extra_fields)       # , role=role
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, role='Admin',dob=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, role=role,dob=dob, **extra_fields)

class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    PATIENT = 'Patient'
    DOCTOR = 'Doctor'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
    ]

    # Fields for custom user roles
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=PATIENT)  # Default role for regular users
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=DOCTOR)
    forget_password_token = models.UUIDField(null=True, blank=True) #forgetpass
    email = models.EmailField(unique=True)
    # objects = CustomUserManager()
    username = models.CharField(max_length=150, unique=True)
    dob = models.DateField(null=True, blank=True)
    # Define boolean fields for specific roles
    # is_patient = models.BooleanField(default=True)
    # is_doctor = models.BooleanField(default=True)
    is_patient=models.BooleanField('is_patient',default=False,null=True)
    is_doctor=models.BooleanField('is_doctor',default=False,null=True)
    REQUIRED_FIELDS=[]
    def __str__(self):
        return self.email
    

# patient
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add fields for id, first name, last name, email, role, dob, and username
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, default=CustomUser.PATIENT)
    dob = models.DateField(null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    
    
# doctor
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add fields for id, first name, last name, email, role, dob, and username
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, default=CustomUser.DOCTOR)
    dob = models.DateField(null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
    
class Medicine(models.Model):
    med_image = models.ImageField(upload_to='shop_images/')
    name = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.CharField(max_length=255)
    company_name = models.CharField(max_length=100)
    medicine_info = models.CharField(max_length=200, default='medicine info')
    quantity = models.PositiveIntegerField(default=0)  # Add this field for quantity

    def __str__(self):
        return self.name
    
    
class DoctorAdditionalDetails(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='doctor_pictures/', null=True, blank=True)
    registration_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    
    
    
User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user}"
    
    def get_total_price(self):
        total = sum(item.subtotal() for item in self.cartitem_set.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.medicine.price
    


# consult
class ConsultationRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='consultation_requests/')
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation request from {self.patient.first_name} to {self.doctor.first_name}"
    
    
class Reply(models.Model):
    consultation_request = models.ForeignKey(ConsultationRequest, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    appointment_needed = models.BooleanField(default=False)

    def __str__(self):
        return f"Reply from {self.doctor.first_name} to {self.consultation_request.patient.first_name}"
    

# appointment
# class Appointment(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     date = models.DateField()
#     time_slot_choices = [
#         ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
#         ('12:00 PM - 1:00 PM', '12:00 PM - 1:00 PM'),
#         ('2:00 PM - 3:00 PM', '2:00 PM - 3:00 PM'),
#         ('4:00 PM - 5:00 PM', '4:00 PM - 5:00 PM'),
#         ('6:00 PM - 7:00 PM', '6:00 PM - 7:00 PM'),
#     ]
#     time_slot = models.CharField(max_length=30, choices=time_slot_choices)
#     patient_name = models.CharField(max_length=60)
#     patient_email = models.EmailField()

#     def __str__(self):
#         return f"Appointment with {self.doctor} on {self.date} at {self.time_slot}"



from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot_choices = [
        ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
        ('12:00 PM - 1:00 PM', '12:00 PM - 1:00 PM'),
        ('2:00 PM - 3:00 PM', '2:00 PM - 3:00 PM'),
        ('4:00 PM - 5:00 PM', '4:00 PM - 5:00 PM'),
        ('6:00 PM - 7:00 PM', '6:00 PM - 7:00 PM'),
    ]
    time_slot = models.CharField(max_length=30, choices=time_slot_choices)
    patient_name = models.CharField(max_length=60)
    patient_email = models.EmailField()

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time_slot}"

    def send_reminders(self):
        today = timezone.now().date()
        appointment_date = self.date
        three_days_before = appointment_date - timedelta(days=3)
        appointment_day = appointment_date

        if today == three_days_before or today == appointment_day:
            subject = f"Reminder: Your appointment with {self.doctor} is tomorrow" if today == three_days_before else f"Reminder: Your appointment with {self.doctor} is today"
            message = f"Dear {self.patient_name},\n\nThis is a reminder for your appointment with {self.doctor} scheduled on {appointment_date} at {self.time_slot}.\n\nPlease ensure you attend the appointment as scheduled.\n\nBest Regards,\nThe Clinic"
            from_email = 'your_email@example.com'
            to_email = self.patient_email

            send_mail(subject, message, from_email, [to_email])

# Signal to trigger reminders when an appointment is saved or updated
@receiver(post_save, sender=Appointment)
def appointment_save_handler(sender, instance, **kwargs):
    instance.send_reminders()
       
    
class Testimonial(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField()

    def __str__(self):
        return f"Testimonial from {self.patient.user.get_full_name()} for Dr. {self.doctor.user.get_full_name()}"
    

    
# class Order(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     order_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order on {self.order_date} for {self.patient.user.get_full_name()} - {self.medicine.name}"

class Order(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order on {self.order_date} for {self.patient.user.get_full_name()} - {self.medicine.name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.medicine.name} in order {self.order.id}"


# clinic work
# class Clinic(models.Model):
#     clinic_name = models.CharField(max_length=100)
#     contact_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     speciality = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)  # Store latitude and longitude as a single field
#     image = models.ImageField(upload_to='clinic_images/')

#     def __str__(self):
#         return self.clinic_name

class Clinic(models.Model):
    clinic_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    speciality = models.CharField(max_length=100)
    location = models.CharField(max_length=100)  # Store latitude and longitude as a single field
    image = models.ImageField(upload_to='clinic_images/')
    doctors = models.ManyToManyField(Doctor, blank=True)  # Many-to-many relationship with Doctor

    def __str__(self):
        return self.clinic_name
    
    
    
    
#chat    
User = get_user_model()

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

class Address(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name