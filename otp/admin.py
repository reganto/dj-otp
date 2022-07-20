from django.contrib import admin

# Register your models here.

from otp.models import User, OTPRequest, Profile

admin.site.register(User)
admin.site.register(OTPRequest)
admin.site.register(Profile)
