from datetime import timedelta
import random
import string
import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.ImageField(verbose_name=_("Avatar"), upload_to="media/images/")

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


class OTPRequest(models.Model):
    class OTPChannel(models.TextChoices):
        ANDROID = _("Android")
        IOS = _("ios")
        WEB = _("Web")

    request_id = models.UUIDField(default=uuid.uuid4, editable=False)
    channel = models.CharField(verbose_name=_("channel"), choices=OTPChannel.choices)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=4, null=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now() + timedelta(seconds=120))
    receipt_id = models.CharField(max_length=255, null=True)

    def generate_password(self):
        self.password = self._random_password()
        self.valid_until = timezone.now() + timedelta(seconds=120)

    def _random_password(self):
        rand = random.choices(string.digits, k=4)
        return "".join(rand)

    class Meta:
        verbose_name = _("One Time Password")
        verbose_name_plural = _("One Time Passwords")
