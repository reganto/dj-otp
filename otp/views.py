from rest_framework.generics import GenericAPIView


class OTPRequestView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        pass


class OTPVerifyView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        pass
