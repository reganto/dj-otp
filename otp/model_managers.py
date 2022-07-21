from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.db import models

from otp import models as otp_models


class OtpQuerySet(models.QuerySet):
    def web(self):
        return self.filter(channel="Web")

    def ios(self):
        return self.filter(channel="ios")

    def android(self):
        return self.filter(channle="android")


class OtpManager(models.Manager):
    def otp_request_exists(self, **kwargs):
        return otp_models.OTPRequest.objects.filter(
            request_id=kwargs.get("request_id"),
            phone=kwargs.get("phone"),
            valid_until__gte=timezone.now(),
        )

    def generate_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token

MyManager = OtpManager.from_queryset(OtpQuerySet)

