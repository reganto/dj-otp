from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

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
    def output_response(self, token, *, new_user):
        return Response(
            VerifyOptResponseSerializer({"token": token, "new_user": True}).data
        )

    def post(self, request, *args, **kwargs):
        serializer = VerifyOptSerializer(data=request.data)
        if serializer.is_valid():
            query = OTPRequest.objects.otp_request_exists(**serializer.validated_data)
            if query.exists():
                User = get_user_model()
                userq = User.objects.filter(
                    username=serializer.validated_data.get("phone")
                )
                if userq.exists():
                    user = userq.first()
                    token = OTPRequest.objects.generate_token(user=user)
                    return self.output_response(token, new_user=False)
                else:
                    user = User.objects.create(
                        username=serializer.validated_data.get("phone")
                    )
                    token = OTPRequest.objects.generate_token(user=user)
                    return self.output_response(token, new_user=True)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
