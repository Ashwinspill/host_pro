from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AllDoctorsListView
from django.contrib.auth.decorators import login_required
from allapp import candy



urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index,name="index"),
    path('index/', views.index,name="index"),
    path('appointment/',views.appointment,name="appointment"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('signup1/',views.signup1,name="signup1"),  #doctor signup
    *candy.path('phome/', views.phome, name='phome'),
    path('dhome/', views.dhome, name='dhome'),
    path('test/', views.test, name='test'),
    path('logout/', views.logout, name='logout'), 
    path('logout_confirmation/', views.logout_confirmation, name='logout_confirmation'),
    path('forget-password/' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('patient_profile/', views.patient_profile, name='patient_profile'), 
    path('patient_profile2/', views.patient_profile2, name='patient_profile2'), 
    path('admind/',views.admind,name="admind"),
    path('toggle-active/<int:user_id>/<str:is_active>/', views.toggle_active, name='toggle_active'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('medicine_list/', views.medicine_list, name='medicine_list'),
    path('patient_medlist/', views.patient_medlist, name='patient_medlist'),
    path('admind/doctor_registration/', views.doctor_registration, name='doctor_registration'),
    path('fill_additional_details/', views.fill_additional_details, name='fill_additional_details'),
    path('doctor_information/', views.doctor_information, name='doctor_information'),
    path('edit_doctor_details/', views.edit_doctor_details, name='edit_doctor_details'),
    path('all_doctors/', AllDoctorsListView.as_view(), name='all_doctors'),
    path('add_to_cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('submit_request/<int:doctor_id>/', views.submit_request, name='submit_request'),
    path('doctor_requests/', views.doctor_request_page, name='doctor_requests'),
    path('doctor_consultation/<int:request_id>/', views.doctor_consultation, name='doctor_consultation'),
    path('patient_replies/', views.patient_replies, name='patient_replies'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('get_available_time_slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('appointment_detail/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('booking_success/', views.booking_success, name='booking_success'),
    path('patient_history/<int:patient_id>/', views.patient_history, name='patient_history'),
    path('checkout/', views.checkout, name='checkout'),
    path('submit_testimonial/<int:doctor_id>/', views.submit_testimonial, name='submit_testimonial'),
    path('doctor_testimonials/<int:doctor_id>/', views.doctor_testimonials, name='doctor_testimonials'),
    path('testimonials/', views.view_testimonials, name='view_testimonials'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('add_clinic/', views.add_clinic, name='add_clinic'),
    path('success/', views.success, name='success'),
    path('clinics/', views.clinic_list, name='clinic_list'),
    path('message_page/', views.message_page, name='message_page'),
    path('clinic/<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('view_location/<int:clinic_id>/', views.view_location, name='view_location'),
    path('quiz/', views.quiz, name='quiz'),
    path('find_nearest_clinic/', views.find_nearest_clinic_view, name='find_nearest_clinic'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('submit_address/', views.submit_address, name='submit_address'),
    path('allergy-types/', views.allergy_types, name='allergy_types'),
    path('outdoor-allergy-types/', views.outdoor_allergy_types, name='outdoor_allergy_types'),
    path('indoor-allergy-types/', views.indoor_allergy_types, name='indoor_allergy_types'),
    path('food-allergy-types/', views.food_allergy_types, name='food_allergy_types'),
    path('skin-allergy-types/', views.skin_allergy_types, name='skin_allergy_types'),
    path('error/', views.error_page, name='error_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)