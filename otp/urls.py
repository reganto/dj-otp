from django.urls import path

from otp import views

urlpatterns = [
    path("request/", views.OTPRequestView.as_view(), name="otp-request"),
    path("verify/", views.OTPVerifyView.as_view(), name="otp-verify"),
]
