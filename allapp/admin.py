from django.contrib import admin
from .models import CustomUser
from .models import Medicine
from .models import Appointment
from .models import ConsultationRequest
from .models import Order
from .models import Testimonial
from .models import DoctorAdditionalDetails
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread, ChatMessage

admin.site.register(ChatMessage)
admin.site.register(CustomUser)
admin.site.register(Medicine)
admin.site.register(Appointment)
admin.site.register(ConsultationRequest)
admin.site.register(Order)
admin.site.register(Testimonial)
admin.site.register(DoctorAdditionalDetails)
# Register your models here.

class ChatMessage(admin.TabularInline):
    model = ChatMessage
    
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)