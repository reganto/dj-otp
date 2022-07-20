# fmt: off
# flake8: noqa

from rest_framework import serializers

from otp.models import OTPRequest


class ReqeustOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices=OTPRequest.OTPChannel.choices)


class ReqeustOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ("request_id",)


class VerifyOptSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=64, allow_null=False)
    phone = serializers.CharField(max_length=12, allow_null=False)
    password = serializers.CharField(allow_null=False)


class VerifyOptResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_user = serializers.BooleanField()
