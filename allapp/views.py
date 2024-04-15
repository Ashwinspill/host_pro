from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from .helpers import send_forget_password_mail
from .forms import PatientProfileForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import check_password
from social_django.models import UserSocialAuth
from django.contrib.auth import login
from social_django.utils import psa
from django.views import View
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import MedicineForm
from .models import Medicine
import razorpay
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from . import candy


# Create your views here.
from .models import Testimonial, Doctor
from django.shortcuts import render

def index(request):
    # Query all Doctor objects
    doctors = Doctor.objects.all()
    testimonials = Testimonial.objects.all()
    
    # Pass the data to the template
    context = {'doctors': doctors, 'testimonials': testimonials}
    
    # Render the HTML template
    return render(request, 'index.html', context)

# @login_required
# def phome(request):
#    if 'email' in request.session:
#        response = render(request, 'phome.html')
#        response['Cache-Control'] = 'no-store, must-revalidate'
#        return response
#    else:
#        return redirect('logout_confirmation') 
 
# def phome(request):
#     if request.user.is_authenticated:
#         response = render(request, 'phome.html')
#         response['Cache-Control'] = 'no-store, must-revalidate'
#         return response
#     else:
#         return redirect('logout_confirmation')
#     # return render(request,'phome.html')
@login_required
def phome(request):
    doctors = Doctor.objects.all()
    testimonials = Testimonial.objects.all()
    
    # Pass the data to the template
    context = {'doctors': doctors, 'testimonials': testimonials}
    response = candy.render(request, 'phome.html', context)
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response    
@login_required
def dhome(request):
    
    doctors = Doctor.objects.all()
    testimonials = Testimonial.objects.all()
    
    # Pass the data to the template
    context = {'doctors': doctors, 'testimonials': testimonials}
    response = render(request, 'dhome.html', context)
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response    

# @login_required
def appointment(request):
    return render(request,'appointment.html')
def test(request):
    return render(request,'test.html')


# #login with google and normal pakka code
# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             # Attempt to retrieve the user by email                                           #pakka sanm 
#             user = CustomUser.objects.get(email=email)

#             # Check the password
#             if user and check_password(password, user.password):
#                 auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Specify the backend
#                 return redirect('phome')
#             else:
#                 error_message = "Invalid credentials"
#                 messages.error(request, error_message)
#         except CustomUser.DoesNotExist:
#             # User with the given email does not exist
#             error_message = "User with this email does not exist"
#             messages.error(request, error_message)

#     response = render(request, 'login.html')
#     response['Cache-Control'] = 'no-store, must-revalidate'
#     return response

    
#testing new login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Attempt to retrieve the user by email
            user = CustomUser.objects.get(email=email)

            # Check the password
            if user and check_password(password, user.password):
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Specify the backend

                # Redirect based on user's role and flags
                if user.is_superuser:
                    return redirect('admind')  # Redirect to admin dashboard
                elif user.is_patient:
                    return redirect('phome')  # Redirect to patient's page
                elif user.is_doctor:
                    return redirect('dhome')  # Redirect to doctor's page
                else:
                    error_message = "Invalid role"
                    messages.error(request, error_message)

            else:
                error_message = "Invalid credentials"
                messages.error(request, error_message)
        except CustomUser.DoesNotExist:
            # User with the given email does not exist
            error_message = "User with this email does not exist"
            messages.error(request, error_message)

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
    
    
    
#patient signup
from .models import CustomUser, Patient

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif password != confirmPassword:
            messages.error(request, "Passwords do not match")
        else:
            # Create a CustomUser with role 'PATIENT'
            user = CustomUser.objects.create_user(
                username=username,
                first_name=firstname,
                last_name=lastname,
                dob=dob,
                email=email,
                password=password,
                is_patient=True,
                role=CustomUser.PATIENT  # Assuming you have defined PATIENT as 'Patient' in your model
            )

            # Create a corresponding Patient record
            Patient.objects.create(
                user=user,
                first_name=firstname,
                last_name=lastname,
                dob=dob,
                email=email,
                username=username
            )

            messages.success(request, "Registered successfully")
            return redirect("login")
    
    return render(request, 'signup.html')

#doctor signup
# def signup1(request):
#     if request.method == "POST":
#         username=request.POST.get('username')
#         #fullname = request.POST.get('firstname')
#         firstname=request.POST.get('firstname') 
#         lastname = request.POST.get('lastname')
#         dob = request.POST.get('dob')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirmPassword = request.POST.get('confirmPassword')
#        # phone_number = request.POST.get('phoneNumber')
#         #address = request.POST.get('address')
      
        

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#         elif CustomUser.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#         elif password != confirmPassword:
#             messages.error(request, "Passwords do not match")
#         else:
#             user = CustomUser(username=username,first_name=firstname,last_name=lastname,dob=dob,email=email,is_doctor=True,role="DOCTOR")  # Change role as needed
#             user.set_password(password)
#             user.save()
#             messages.success(request, "Registered successfully")
#             return redirect("login")
#     return render(request,'signup1.html')



# new doctor signup 
from .models import CustomUser, Doctor
def signup1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        # Check if the email or username already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif password != confirmPassword:
            messages.error(request, "Passwords do not match")
        else:
            # Create a CustomUser with role 'DOCTOR'
            user = CustomUser.objects.create_user(
                username=username,
                first_name=firstname,
                last_name=lastname,
                dob=dob,
                email=email,
                password=password,
                is_doctor=True,
                role=CustomUser.DOCTOR  # Assuming you have defined DOCTOR as 'Doctor' in your model
            )

            # Create a corresponding Doctor record
            Doctor.objects.create(
                user=user,
                first_name=firstname,
                last_name=lastname,
                dob=dob,
                email=email,
                username=username
            )

            messages.success(request, "Registered successfully")
            return redirect("login")
    
    return render(request, 'signup1.html')

@never_cache
def logout_confirmation(request):
    return render(request, 'logout_confirmation.html')
@login_required
def logout(request):
    auth_logout(request) # Use the logout function to log the user out
    return redirect('logout_confirmation')  # Redirect to the confirmation page

def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = CustomUser.objects.filter(forget_password_token=token).first()

        if profile_obj is None:
            messages.error(request, 'Invalid token.')
            return redirect('/forget-password/')

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect(f'/change-password/{token}/')

            # Update the password for the user associated with profile_obj
            profile_obj.set_password(new_password)
            profile_obj.forget_password_token = None  # Remove the token
            profile_obj.save()

            # Set a success message
            messages.success(request, 'Password changed successfully.')

            # Redirect to login page with the success message
            return redirect('/login/', {'success_message': 'Password changed successfully'})

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred while processing your request.')
    
    return render(request, 'change-password.html', context)

import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            user_obj = CustomUser.objects.filter(username=username).first()
            
            if user_obj is None:
                messages.error(request, 'No user found with this username.')
                return redirect('/forget-password/')
            
            token = str(uuid.uuid4())
            user_obj.forget_password_token = token
            user_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('/forget-password/')
    
    except Exception as e:
        print(e)
    
    return render(request, 'forget-password.html')
# @login_required
@never_cache
def patient_profile(request):
    patient = request.user
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
    else:
        form = PatientProfileForm(instance=patient)

    return render(request, 'patient_profile.html', {'patient': patient, 'form': form})


# trial of profile 
# class PatientProfileForm(forms.ModelForm):
#     dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email', 'username', 'dob']

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         # Add your email validation logic here, e.g., check for a specific domain or pattern
#         if not email.endswith('@example.com'):
#             raise forms.ValidationError("Email must be from example.com domain.")
#         return email

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         # Add your username validation logic here, e.g., checking for uniqueness
#         if CustomUser.objects.filter(username=username).exclude(id=self.instance.id).exists():
#             raise forms.ValidationError("Username is already in use.")
#         return username

#     def clean_dob(self):
#         dob = self.cleaned_data.get('dob')
#         # Add your date of birth validation logic here, e.g., checking if the user is of a certain age
#         # Example: Check if the user is at least 18 years old
#         from datetime import date
#         age = date.today().year - dob.year
#         if age < 18:
#             raise forms.ValidationError("You must be at least 18 years old.")
#         return dob

@never_cache
def patient_profile2(request):
    patient = request.user
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
    else:
        form = PatientProfileForm(instance=patient)

    return render(request, 'patient_profile2.html', {'patient': patient, 'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Testimonial, Order

# @login_required
# def admind(request):
#     # Query all User objects (using the custom user model) from the database
#     User = get_user_model()
#     user_profiles = User.objects.all()
    
#     # Query Testimonial objects
#     testimonials = Testimonial.objects.all()
    
#     # Perform sentiment analysis for each testimonial
#     for testimonial in testimonials:
#         sentiment_score, sentiment_label = analyze_sentiment(testimonial.feedback)
#         testimonial.sentiment_score = sentiment_score
#         testimonial.sentiment_label = sentiment_label

#     # Query Order objects
#     orders = Order.objects.all()

#     # Pass the data to the template
#     context = {
#         'user_profiles': user_profiles,
#         'testimonials': testimonials,
#         'orders': orders,
#     }
    
#     # Render the HTML template
#     response = render(request, 'admind.html', context)
#     response['Cache-Control'] = 'no-store, must-revalidate'
#     return response

@login_required
def admind(request):
    # Query all User objects (using the custom user model) from the database
    User = get_user_model()
    user_profiles = User.objects.all()
    
    # Query Testimonial objects
    testimonials = Testimonial.objects.all()
    
    # Perform sentiment analysis for each testimonial and filter based on sentiment
    filtered_testimonials = []
    for testimonial in testimonials:
        sentiment_score, sentiment_label = analyze_sentiment(testimonial.feedback)
        testimonial.sentiment_score = sentiment_score
        testimonial.sentiment_label = sentiment_label
        
        # Filter testimonials based on sentiment
        if request.GET.get('sentiment') == 'positive' and sentiment_score > 0:
            filtered_testimonials.append(testimonial)
        elif request.GET.get('sentiment') == 'negative' and sentiment_score < 0:
            filtered_testimonials.append(testimonial)
        elif not request.GET.get('sentiment'):
            filtered_testimonials.append(testimonial)

    # Query Order objects
    orders = Order.objects.all()

    # Pass the data to the template
    context = {
        'user_profiles': user_profiles,
        'filtered_testimonials': filtered_testimonials,
        'orders': orders,
    }
    
    # Render the HTML template
    response = render(request, 'admind.html', context)
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response


def toggle_active(request, user_id, is_active):
    user = get_object_or_404(CustomUser, id=user_id)
    is_active = is_active.lower() == 'true'

    if is_active:  # If activating the user
        # Send an activation email
        subject = 'Your Account Deactivation'
        message = 'Your account has been Deactivated. Please contact support for more information.'
    else:  # If deactivating the user
        # Send a deactivation email
        subject = 'Your Account Activation'
        message = 'Your account has been Activated by the administrator. You can now log in and use your account.'

    from_email = 'allergycare163@gmail.com'  # Use the email address you configured in settings.py
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        user.is_active = not is_active
        user.save()

        response_data = {
            'message': f'User is now {"Active" if user.is_active else "Inactive"}.',
            'email_sent': True
        }
    except CustomUser.DoesNotExist:
        response_data = {
            'message': 'User not found',
            'email_sent': False
        }

    return JsonResponse(response_data)


def google_authenticate(request):
    # Handle the Google OAuth2 authentication process
    # ...

    # After successful authentication, create or get the user
    try:
        user_social = UserSocialAuth.objects.get(provider='google-oauth2', user=request.user)
        user = user_social.user
    except UserSocialAuth.DoesNotExist:
        user = request.user

    # Set the user's role to "Patient"
        user.role = 'Patient'
        user.save()

    # Set the user's is_patient field to True
        user.is_patient = True
        user.save()

    # Redirect to the desired page (phome.html for Patient role)
    return redirect('phome')  # Make sure you have a URL named 'phome

# def add_medicine(request):
#     if request.method == 'POST':
#         form = MedicineRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('medicine_list')  # Redirect to the medicine list page
#     else:
#         form = MedicineRegistrationForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'add_medicine.html', context)

@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')  # Redirect to the medicine list page
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

@login_required
def patient_medlist(request):
    medicines = Medicine.objects.all()
    return render(request, 'patient_medlist.html', {'medicines': medicines})



# from .forms import DoctorDetailsForm
# def add_doctor_details(request):
#     if request.method == 'POST':
#         user = request.user
#         # Check if a DoctorDetails instance already exists for this user
#         if not hasattr(user, 'doctor_details'):
#             form = DoctorDetailsForm(request.POST, request.FILES)
#             if form.is_valid():
#                 doctor_details = form.save(commit=False)
#                 doctor_details.user = user
#                 doctor_details.save()
#                 return redirect('doctor_information')
#         else:
#             form = DoctorDetailsForm()
#     return render(request, 'doctor_information.html', {'form': form})



# doctor by admin starts here 
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
@login_required
def doctor_registration(request):
    if request.method == 'POST':
        provider_name = request.POST.get('providername')
        provider_email = request.POST.get('email')
        
        # Validate the input fields here if necessary
        
        # Replace 'YOUR_BASE_URL' with the actual base URL of your website
        base_url = 'http://127.0.0.1:8000/signup1'
        
        # Create a registration link
        registration_path = "register"  # Relative path for registration
        registration_link = f"{base_url}"
        
        # Render HTML content for the email
        html_message = render_to_string('doctor_registration_email.html', {
            'provider_name': provider_name,
            'registration_link': registration_link
        })
        
        # Send HTML email to the provider's email
        subject = 'Doctor Registration Link'
        plain_message = f"Click the following link to complete your registration: {registration_link}"
        from_email = settings.DEFAULT_FROM_EMAIL
        
        email = EmailMessage(subject, plain_message, from_email, [provider_email])
        email.content_subtype = "html"
        email.send(fail_silently=False)
        
        # Redirect to a success page or display a success message
        return render(request, 'doctor_registration_success.html')
    
    return render(request, 'doctor_registration_form.html')


from .forms import DoctorAdditionalDetailsForm
from .models import Doctor
@login_required
def fill_additional_details(request):
    if request.method == "POST":
        form = DoctorAdditionalDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            doctor_instance = Doctor.objects.get(user=request.user)  # Get the currently logged-in doctor

            # Create and save the DoctorAdditionalDetails instance using the form
            doctor_additional_details = form.save(commit=False)  # Create an instance without saving it
            doctor_additional_details.doctor = doctor_instance  # Link it to the doctor
            doctor_additional_details.save()

            return redirect('doctor_information')  # Redirect to the doctor information page

    else:
        form = DoctorAdditionalDetailsForm()

    return render(request, 'fill_additional_details.html', {'form': form})


from django.http import HttpResponse
from .models import Doctor, DoctorAdditionalDetails
@login_required
def doctor_information(request):
    if request.user.is_authenticated and request.user.is_doctor:
        # Get the doctor and associated additional details if they exist
        try:
            doctor = Doctor.objects.get(user=request.user)
            additional_details = DoctorAdditionalDetails.objects.get(doctor=doctor)
        except Doctor.DoesNotExist:
            doctor = None
            additional_details = None

        return render(request, 'doctor_info.html', {'doctor': doctor, 'additional_details': additional_details})
    else:
        return HttpResponse("User is not authenticated or not a doctor.")
    
    

from .forms import DoctorForm, DoctorAdditionalDetailsForm
@login_required
def edit_doctor_details(request):
    user = request.user
    try:
        doctor = Doctor.objects.get(user=user)
        doctor_additional_details = DoctorAdditionalDetails.objects.get(doctor=doctor)
    except Doctor.DoesNotExist:
        # Handle the case where the doctor doesn't exist
        # You can create a doctor profile if needed
        return redirect('create_doctor_profile')
    
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, instance=doctor)
        details_form = DoctorAdditionalDetailsForm(request.POST, request.FILES, instance=doctor_additional_details)
        if doctor_form.is_valid() and details_form.is_valid():
            doctor_form.save()
            details_form.save()
            return redirect('doctor_information')
    else:
        doctor_form = DoctorForm(instance=doctor)
        details_form = DoctorAdditionalDetailsForm(instance=doctor_additional_details)
    
    return render(request, 'edit_doctor_details.html', {'doctor_form': doctor_form, 'details_form': details_form})


from django.views.generic import ListView
from .models import Doctor, DoctorAdditionalDetails

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
    
    
    
# cart trial
from .models import Medicine, Cart, CartItem
@login_required
def add_to_cart(request, medicine_id):
    if request.method == 'POST':
        # Get the medicine object based on the medicine_id
        medicine = Medicine.objects.get(pk=medicine_id)
        user = request.user  # Assuming the user is authenticated

        # Check if the user has a cart, create one if not
        cart, created = Cart.objects.get_or_create(user=user)

        # Check if the medicine is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)

        if not item_created:
            # If the item already exists in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()

        # Reduce the quantity of the medicine in your inventory
        medicine.quantity -= 1
        medicine.save()

    return redirect('view_cart')  # Redirect to the cart view after adding the item




from django.http import HttpResponse

@login_required
def view_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)

    # Calculate subtotal for each cart item
    for cart_item in cart.cartitem_set.all():
        cart_item.subtotal = cart_item.quantity * cart_item.medicine.price

    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)

from .models import Address

@login_required
def submit_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        pin_code = request.POST.get('pin_code')
        address_text = request.POST.get('address')
        district = request.POST.get('district')
        state = request.POST.get('state')

        # Get the current user
        user = request.user

        # Create the address object
        address_obj = Address.objects.create(
            patient=user,
            name=name,
            mobile_number=mobile_number,
            pin_code=pin_code,
            address=address_text,
            district=district,
            state=state
        )
        
        # Redirect to the cart page
        return redirect('view_cart')
     
    return render(request, 'cart.html')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)

    # Increase the quantity of the medicine in your inventory
    cart_item.medicine.quantity += 1
    cart_item.medicine.save()

    cart_item.delete()

    return redirect('view_cart')


from decimal import Decimal
import razorpay
@login_required
def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    amount = cart.get_total_price()
    amount_in_paise = int(amount * 100)  # Convert to integer

    DATA = {
        "amount": amount_in_paise,  # Use the integer value
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }

    client = razorpay.Client(auth=("rzp_test_aWcyAl6q9LJYqx", "j1dFxiB5MzxmkXTMo6IYQlnP"))
    payment = client.order.create(data=DATA)
    
    address = Address.objects.filter(patient=user).first()

    context = {
        'cart': cart,
        'total': cart.get_total_price(),
        'amount': amount_in_paise,  # Pass the integer value to the context
        'payment': payment,
        'address': address,
    }
    return render(request, 'checkout.html', context)



from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Patient, Order
from .models import CartItem, Cart  # Assuming you have Cart and CartItem models
from reportlab.pdfgen import canvas
from decimal import Decimal
from django.db.models import Sum
from datetime import datetime


from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone
from .models import CartItem, Order, Medicine, Cart  # Import necessary models
from reportlab.lib.units import inch
@login_required
@csrf_exempt
def payment_success(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart__user=user)

    # Calculate total amount paid using aggregate
    total_amount_paid = cart_items.aggregate(total_amount_paid=Sum('medicine__price'))['total_amount_paid'] or 0

    # Create an order after successful payment
    order = Order.objects.create(
        patient=patient,
        amount_paid=total_amount_paid,
    )

    # Add individual items to the order
    for cart_item in cart_items:
        order.orderitem_set.create(
            medicine=cart_item.medicine,
            quantity=cart_item.quantity,
            subtotal=cart_item.subtotal(),
        )

    # Clear the patient's cart after creating the order
    cart_items.delete()

    # Create PDF bill
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    data = []
    data.append(["Medicine", "Quantity", "Price", "Subtotal"])

    for order_item in order.orderitem_set.all():
        data.append([order_item.medicine.name, order_item.quantity, order_item.medicine.price, order_item.subtotal])

    # Create table with thicker borders
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black),
                               ('BOX', (0, 0), (-1, -1), 2, colors.black)]))  # Thick border

    # Increase table size
    table._argW[0] = 2.5 * inch  # Adjust width of the first column
    table._argW[1] = 1.5 * inch  # Adjust width of the second column
    table._argW[2] = 1 * inch    # Adjust width of the third column
    table._argW[3] = 1.5 * inch  # Adjust width of the fourth column

    # Add table to PDF
    pdf_title = Paragraph("AllergyCare - Your Allergy Management Solution", styles['Title'])
    pdf_issued_date = Paragraph(f"Issued on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic'])
    pdf_total_amount_paid = Paragraph(f"Total Amount Paid: Rs.{total_amount_paid}", styles['BodyText'])

    elements = [pdf_title, pdf_issued_date, table, pdf_total_amount_paid]
    pdf.build(elements)

    # Get PDF content
    pdf_data = buffer.getvalue()
    buffer.close()

    # Prepare response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{order.order_date.strftime("%Y%m%d%H%M%S")}.pdf"'
    response.write(pdf_data)

    messages.success(request, 'Payment successful! Your order has been placed.')
    return response

#online consulting
from .forms import ConsultationRequestForm
@login_required
def submit_request(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = ConsultationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            consultation_request = form.save(commit=False)
            consultation_request.patient = request.user.patient
            consultation_request.doctor = doctor
            consultation_request.save()
            return redirect('all_doctors')  # Redirect to the doctor list after submission

    else:
        form = ConsultationRequestForm()

    return render(request, 'submit_request.html', {'form': form})


from .models import ConsultationRequest
@login_required
class DoctorRequestsListView(ListView):
    model = ConsultationRequest
    template_name = 'doctor_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return ConsultationRequest.objects.filter(doctor=self.request.user.doctor)
    
@login_required
def doctor_request_page(request):
    # Retrieve consultation requests for the logged-in doctor
    consultation_requests = ConsultationRequest.objects.filter(doctor=request.user.doctor)
    
    return render(request, 'doctor_request_page.html', {'requests': consultation_requests})


from .forms import ConsultationForm
from .models import ConsultationRequest, Reply

@login_required
def doctor_consultation(request, request_id):
    consultation_request = ConsultationRequest.objects.get(pk=request_id)
    # replies = Reply.objects.filter(consultation_request=consultation_request).order_by('-timestamp')
    replies = Reply.objects.filter(consultation_request=consultation_request)

    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            consultation_fee = form.cleaned_data['consultation_fee']
            appointment_needed = form.cleaned_data['appointment_needed']

            # Create a new Reply and save it
            reply = Reply(consultation_request=consultation_request, doctor=request.user.doctor, message=message, consultation_fee=consultation_fee, appointment_needed=appointment_needed)
            reply.save()

            # Redirect back to the same consultation page after submitting the reply
            return redirect('doctor_consultation', request_id)

    else:
        form = ConsultationForm()

    return render(request, 'doctor_consultation.html', {'form': form, 'consultation_request': consultation_request, 'replies': replies})

# @login_required
# def patient_replies(request):
#     # Query the replies for the current patient (you'll need to identify the patient, e.g., using the logged-in user)
#     patient_replies = Reply.objects.filter(consultation_request__patient=request.user.patient)

#     return render(request, 'patient_replies.html', {'replies': patient_replies})

# def patient_replies(request):
#     replies = Reply.objects.all()  # Assuming you have a queryset of replies
#     context = {'replies': replies}
#     return render(request, 'patient_replies.html', context)

from .models import Reply
from django.shortcuts import render

@login_required
def patient_replies(request):
    replies = Reply.objects.all()
    
    # Assuming you have a queryset of replies
    # Update the line below to get the correct consultation_fee
    amount = replies[0].consultation_fee  # You might need to adjust this based on your model structure
    
    amount_in_paise = int(amount * 100)  # Convert to integer

    DATA = {
        "amount": amount_in_paise,  # Use the integer value
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }

    client = razorpay.Client(auth=("rzp_test_aWcyAl6q9LJYqx", "j1dFxiB5MzxmkXTMo6IYQlnP"))
    payment = client.order.create(data=DATA)

    context = {
        'amount': amount_in_paise,  # Pass the integer value to the context
        'payment': payment,
        'replies': replies
    }

    return render(request, 'patient_replies.html', context)


from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment, Doctor
from .forms import AppointmentForm
from django.core.mail import send_mail
from django.template.loader import render_to_string


@login_required
def create_appointment(request):
    if request.method == 'POST':
        # Get the doctor instance
        doctor_id = request.GET.get('doctor_id')
        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Automatically populate patient name and email
        patient = request.user.patient
        form_data = request.POST.copy()
        form_data['patient_name'] = f"{patient.first_name} {patient.last_name}"  # Concatenate first name and last name
        form_data['patient_email'] = patient.email

        form = AppointmentForm(form_data)
        
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor  # Assign the doctor to the appointment
            appointment.patient_name = form_data['patient_name']  # Set patient_name from form_data
            appointment.patient_email = form_data['patient_email']  # Set patient_email from form_data
            date = appointment.date
            time_slot = appointment.time_slot

            # Check if the slot is available for the selected doctor and date
            slot_exists = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time_slot=time_slot
            ).exists()

            if not slot_exists:
                # Check if the patient already has an appointment on the same day
                existing_appointment = Appointment.objects.filter(
                    patient=patient,
                    date=date
                ).first()

                if existing_appointment:
                    messages.error(request, 'You already have an appointment on the same day.')
                else:
                    # Process payment and create appointment
                    amount = int(5 * 100)  # Example amount in paise
                    
                    # Generate Razorpay payment order
                    client = razorpay.Client(auth=("rzp_test_aWcyAl6q9LJYqx", "j1dFxiB5MzxmkXTMo6IYQlnP"))
                    payment = client.order.create(data={
                        "amount": amount,
                        "currency": "INR",
                        "receipt": "appointment_" + str(appointment.pk),  # Unique receipt identifier
                        "notes": {
                            "patient_name": form_data['patient_name'],  # Use the concatenated full name
                            "appointment_date": str(date),
                            "appointment_time": time_slot,
                            "doctor_name": f"{doctor.first_name} {doctor.last_name}"  # Concatenate doctor's first name and last name
                        }
                    })
                    
                    # Pass payment ID to the template for Razorpay checkout
                    payment_id = payment['id']

                    # Save appointment after successful payment
                    appointment.patient = patient
                    appointment.save()

                    # Send email confirmation
                    subject = 'Appointment Confirmation'
                    from_email = 'your_email@example.com'
                    to_email = patient.email
                    appointment_data = {
                        'appointment': appointment,
                    }

                    html_message = render_to_string('appointment_email.html', appointment_data)
                    plain_message = strip_tags(html_message)

                    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

                    # Redirect to the booking_success page upon successful appointment
                    return redirect('booking_success')
            else:
                messages.error(request, 'This slot is already booked. Please choose another.')

    else:
        form = AppointmentForm()

    return render(request, 'create_appointment.html', {'form': form})



    
@login_required   
def booking_success(request):
    return render(request, 'booking_success.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Appointment

@login_required
def view_appointments(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'view_appointments.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    doctor = appointment.doctor

    # Send cancellation email to the doctor
    subject = f'Appointment Cancelled - {appointment}'
    message = f'The appointment with {doctor} scheduled for {appointment.date} at {appointment.time_slot} has been cancelled. Your Initial Payment will be  as service charge'
    from_email = 'your_email@example.com'
    to_email = doctor.email
    send_mail(subject, message, from_email, [to_email])

    # Delete the appointment
    appointment.delete()
    
    messages.success(request, 'Booking has been cancelled.')

    return redirect('view_appointments')




@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

@login_required
def list_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'list_appointments.html', {'appointments': appointments})

@login_required
def get_available_time_slots(request):
    if request.is_ajax() and request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        selected_date = request.POST.get("selected_date")

        # Retrieve the doctor's appointments for the selected date
        appointments = Appointment.objects.filter(
            doctor_id=doctor_id,
            date=selected_date,
        )

        # Extract the booked time slots
        booked_slots = [appointment.time_slot for appointment in appointments]

        # Define a list of all available time slots
        all_time_slots = ["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM", "07:00 PM"]  # Define your time slots

        # Calculate available time slots by removing booked slots
        available_slots = [slot for slot in all_time_slots if slot not in booked_slots]

        return JsonResponse({"available_slots": available_slots})
    return JsonResponse({"error": "Invalid request"}, status=400)




# history
from .models import Appointment, ConsultationRequest
@login_required
def patient_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Query the patient's appointment history
    appointments = Appointment.objects.filter(patient=patient)
    
    # Query the patient's consultation request history
    consultation_requests = ConsultationRequest.objects.filter(patient=patient)
    
    return render(request, 'patient_history.html', {'patient': patient, 'appointments': appointments, 'consultation_requests': consultation_requests})




#testimony
from .models import Testimonial
from .forms import TestimonialForm  # Create a form for testimonials

@login_required
def submit_testimonial(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.doctor = doctor
            testimonial.patient = request.user.patient  # Assuming you have a Patient model
            testimonial.save()
            messages.success(request, 'Testimonial submitted successfully!')
            return redirect('all_doctors')
        else:
            messages.error(request, 'Error submitting testimonial. Please check the form.')
    else:
        form = TestimonialForm()

    return render(request, 'submit_testimonial.html', {'form': form, 'doctor': doctor})



from textblob import TextBlob


def analyze_sentiment(feedback):
    """
    Analyzes the sentiment of the given feedback using TextBlob.
    Returns a tuple containing the sentiment score and label.
    """
    # Create a TextBlob object
    blob = TextBlob(feedback)
    
    # Get the sentiment score (-1 for negative, 0 for neutral, 1 for positive)
    sentiment_score = blob.sentiment.polarity
    
    # Determine the sentiment label
    if sentiment_score > 0:
        sentiment_label = 'Positive'
    elif sentiment_score < 0:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    
    return sentiment_score, sentiment_label


@login_required
def view_testimonials(request):
    testimonials = Testimonial.objects.all()
    
    # Analyze sentiment for each testimonial
    for testimonial in testimonials:
        sentiment_score, sentiment_label = analyze_sentiment(testimonial.feedback)
        testimonial.sentiment_score = sentiment_score
        testimonial.sentiment_label = sentiment_label
    
    return render(request, 'view_testimonials.html', {'testimonials': testimonials})



from .models import Doctor, Testimonial
@login_required
def doctor_testimonials(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    testimonials = Testimonial.objects.filter(doctor=doctor)

    return render(request, 'doctor_testimonials.html', {'doctor': doctor, 'testimonials': testimonials})


from .forms import ClinicForm

@login_required
def add_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            clinic = form.save(commit=False)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            clinic.location = f"{latitude}, {longitude}"
            
            # Process selected doctors
            doctors_ids = request.POST.getlist('doctors')  # Get the list of selected doctors' IDs
            clinic.save()  # Save the clinic first to get its ID
            
            # Associate selected doctors with the clinic
            for doctor_id in doctors_ids:
                doctor = Doctor.objects.get(pk=doctor_id)
                clinic.doctors.add(doctor)
            
            clinic.save()  # Save the clinic again after adding doctors
            messages.success(request, 'Clinic added successfully!')
            return redirect('add_clinic')  # Redirect back to the same page after successful submission
        else:
            # Print form errors for debugging
            print(form.errors)
            # Print POST data for debugging
            print(request.POST)
            # Return HttpResponse with form errors for debugging
            return HttpResponse("Form is not valid. Errors: " + str(form.errors))
    else:
        form = ClinicForm()
        doctors = Doctor.objects.all()  # Retrieve all doctors
    return render(request, 'add_clinic.html', {'form': form, 'doctors': doctors})


#clinic_details
@login_required
def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, pk=clinic_id)
    return render(request, 'clinic_detail.html', {'clinic': clinic})

@login_required
def view_location(request, clinic_id):
    clinic = get_object_or_404(Clinic, pk=clinic_id)
    latitude, longitude = clinic.location.split(',')
    google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    return redirect(google_maps_url)

@login_required
def success(request):
    return render(request, 'success.html')

from .models import Clinic
@login_required
def clinic_list(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinic_list.html', {'clinics': clinics})

from .models import Thread
@login_required
def message_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)




from django.http import JsonResponse, HttpResponse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from django.shortcuts import render

@login_required
def quiz(request):
    if request.method == 'POST':
        # Store form submission data in a variable
        form_data = request.POST
        print("Form data:", form_data)  # Debugging statement

        # Load data
        data = pd.read_csv(r'C:/Users/ashwin/Desktop/mini/symp.csv')

        # # Print data corresponding to each question
        # print("Data for each question:")
        # for column in data.columns:
        #     print(f"{column}: {data[column].unique()}")

        # Drop rows with missing 'Result' values
        data.dropna(subset=['Result'], inplace=True)

        # Check if there are any missing values in the target variable y
        if data['Result'].isnull().any():
            return HttpResponse("Error: Target variable 'Result' contains missing values")

        # Preprocess data (convert categorical variables to numerical)
        data['Sore or Watery Eyes'] = data['Sore or Watery Eyes'].map({'Yes': 1, 'No': 0})
        data['Symptoms Outdoors'] = data['Symptoms Outdoors'].map({'Yes': 1, 'No': 0})
        data['Symptoms Time of Year'] = data['Symptoms Time of Year'].map({'All year': 1, 'Certain Season': 0})
        data['Breathing Problems around Smoke'] = data['Breathing Problems around Smoke'].map({'Yes': 1, 'No': 0})
        data['Symptoms with Furry Pets'] = data['Symptoms with Furry Pets'].map({'Yes': 1, 'No': 0})
        data['Reaction to Dairy'] = data['Reaction to Dairy'].map({'Yes': 1, 'No': 0})
        data['Reaction to Food'] = data['Reaction to Food'].map({'Yes': 1, 'No': 0})

        # Drop unnamed columns
        data.drop(data.columns[data.columns.str.contains('Unnamed', case=False)], axis=1, inplace=True)

        # Define features and target
        X = data.drop('Result', axis=1)
        y = data['Result']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Evaluate model
        accuracy = model.score(X_test, y_test)

        # Extract user responses from the form data variable
        responses = [
            1 if form_data.get('q1') == 'yes' else 0,  # Map 'Yes' to 1 and 'No' to 0
            1 if form_data.get('q2') == 'yes' else 0,  # Map 'Yes' to 1 and 'No' to 0
            1 if form_data.get('q3') == 'all_year' else 0,  # Map 'All year' to 1 and 'Certain Season' to 0
            1 if form_data.get('q4') == 'yes' else 0,  # Map 'Yes' to 1 and 'No' to 0
            1 if form_data.get('q5') == 'yes' else 0,  # Map 'Yes' to 1 and 'No' to 0
            1 if form_data.get('q6') == 'yes' else 0,  # Map 'Yes' to 1 and 'No' to 0
            1 if form_data.get('q7') == 'yes' else 0,  # Map 'Yes' to 1 and 'No' to 0
        ]

        # Make prediction
        prediction = model.predict([responses])[0]

        print("Prediction:", prediction)  # Debugging statement
        print("Responses:", responses)  # Debugging statement

        # Assign initial value to result_label
        result_label = ""

        # Map prediction back to original label
        if prediction == 1:
            result_label = 'It looks like you may have allergies pertaining to indoor or outdoor triggers. Given by some of your responses, you may also be allergic to certain kinds of food.'
        elif prediction == 2:
            result_label = 'You may have a non-pollen related allergy, for example to house dust, pets or mold.'
        elif prediction == 3:
            result_label = "Sorry we couldn't find the problem."
        elif prediction == 4:
            result_label = 'Your seasonal profile suggests that you may be affected by weed pollen and might also be affected by mold or fungal spores. These are widespread in certain seasons.'
        else:
            result_label = "Unknown prediction"  # Adding a default value if prediction does not match any condition

        # Return prediction and evaluation as JSON response
        return JsonResponse({'result': prediction, 'accuracy': accuracy})

    return render(request, 'quiz.html')





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .utils import find_nearest_clinic
from .models import Clinic

@login_required
def find_nearest_clinic_view(request):
    if request.method == 'POST':
        # Get the latitude and longitude from the form POST data
        latitude_str = request.POST.get('latitude')
        longitude_str = request.POST.get('longitude')

        # Validate latitude and longitude inputs
        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)
        except ValueError:
            return HttpResponseBadRequest("Invalid latitude or longitude value")

        # Get clinic locations and names
        clinic_data = [(clinic.clinic_name, float(clinic.location.split(',')[0]), float(clinic.location.split(',')[1])) for clinic in Clinic.objects.all()]

        # Call the utility function to find the nearest clinic
        nearest_clinic, min_distance, clinic_name = find_nearest_clinic(latitude, longitude, clinic_data)
        
        # Pass the data to the template
        return render(request, 'nearest_clinic.html', {'nearest_clinic': nearest_clinic, 'min_distance': min_distance, 'clinic_name': clinic_name})
    else:
        return render(request, 'location_form.html')


from .models import Appointment
from .forms import AppointmentForm

@login_required
def doctor_appointments(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor)

    if request.method == 'POST':
        if 'reschedule' in request.POST:
            # Handle appointment rescheduling
            appointment_id = request.POST.get('appointment_id')
            appointment = Appointment.objects.get(pk=appointment_id)
            form = AppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                form.save()
                return redirect('doctor_appointments')

    else:
        form = AppointmentForm()

    context = {
        'appointments': appointments,
        'form': form
    }
    return render(request, 'doctor_appointments.html', context)


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm

@login_required
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            # Update the appointment date and time slot
            appointment.date = form.cleaned_data['date']
            appointment.time_slot = form.cleaned_data['time_slot']
            appointment.save()
            
            # Send email notification to the patient
            send_reschedule_email(appointment.patient_email, appointment.doctor.first_name, appointment.date)
            
            return redirect('doctor_appointments')
    else:
        form = AppointmentForm(instance=appointment)

    context = {
        'form': form,
        'appointment': appointment
    }
    return render(request, 'reschedule_appointment.html', context)

def send_reschedule_email(patient_email, doctor_name, new_date):
    subject = 'Appointment Rescheduled'
    message = f'Your appointment with Dr. {doctor_name} has been rescheduled to {new_date} due to an emergency.'
    sender_email = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, message, sender_email, [patient_email])
    except Exception as e:
        # Log or handle the error
        print(f"Error sending email: {e}")
        
        
@login_required       
def allergy_types(request):
    return render(request, 'allergy_types.html')

@login_required
def outdoor_allergy_types(request):
    return render(request, 'outdoor_allergy_types.html')
@login_required
def indoor_allergy_types(request):
    return render(request, 'indoor_allergy_types.html')
@login_required
def food_allergy_types(request):
    return render(request, 'food_allergy_types.html')
@login_required
def skin_allergy_types(request):
    return render(request, 'skin_allergy_types.html')
@login_required
def error_page(request):
    error_message = "An error occurred. Please try again later."  # You can customize this message as needed
    return render(request, 'error_page.html', {'message': error_message})