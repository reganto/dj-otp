from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from otp.serializers import (
    ReqeustOTPSerializer,
    ReqeustOTPResponseSerializer,
    VerifyOptSerializer,
    VerifyOptResponseSerializer,
)
from otp.throttles import OncePerMinuteThrottle
from otp.models import OTPRequest


class OTPRequestView(GenericAPIView):
    throttle_classes = (OncePerMinuteThrottle,)

    def post(self, request, *args, **kwargs):
        serializer = ReqeustOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_req = OTPRequest()
            otp_req.save(**serializer.validated_data)
            # SMS API call
            return Response(ReqeustOTPResponseSerializer(otp_req).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyOptSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: convert this query to a queryset or manager
            query = OTPRequest.objects.filter(
                request_id=serializer.validated_data.get("request_id"),
                phone=serializer.validated_data.get("phone"),
                valid_until__gte=timezone.now(),
            )
            if query.exists():
                User = get_user_model()
                userq = User.objects.filter(
                    username=serializer.validated_data.get("phone")
                )
                if userq.exists():
                    user = userq.first()
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        VerifyOptResponseSerializer(
                            {"token": token, "new_user": False}
                        ).data
                    )
                else:
                    user = User.objects.create(
                        username=serializer.validated_data.get("phone")
                    )
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        VerifyOptResponseSerializer(
                            {"token": token, "new_user": True}
                        ).data
                    )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
