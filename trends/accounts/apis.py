from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from trends.accounts.models import User, Profile
from trends.accounts.services import register, update_profile
from trends.accounts.validators import (
    digits_validator,
    letters_validator,
    special_char_validator
)
from .selectors import get_profile


class RegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        fullname = serializers.CharField(max_length=255)
        password = serializers.CharField(
            max_length=255,
            validators=[
                digits_validator,
                letters_validator,
                special_char_validator,
                MinLengthValidator(limit_value=10)
            ])
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email: str):
            # TODO: check all emails with dots

            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError("Email already exists!")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    class OutputRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('email', 'token')

        token = serializers.SerializerMethodField(read_only=True)

        def get_token(self, *args, **kwargs):
            return "temporary-jwt-token"

    @extend_schema(request=InputRegisterSerializer, responses=InputRegisterSerializer)
    def post(self, request):
        serializer_obj = self.InputRegisterSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)

        try:
            user = register(
                email=serializer_obj.validated_data.get("email"),
                password=serializer_obj.validated_data.get("password"),
                fullname=serializer_obj.validated_data.get("fullname"),

            )
        except Exception as e:
            return Response(
                f"Database Error {e}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputRegisterSerializer(user).data)


class ProfileApi(APIView):
    class InputProfileSerializer(serializers.Serializer):
        fullname = serializers.CharField(max_length=255)
        about = serializers.CharField()

    class OutputProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('fullname', 'about')

    @extend_schema(request=InputProfileSerializer, responses=InputProfileSerializer)
    def put(self, request):
        serializer_obj = self.InputProfileSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        try:
            profile = update_profile(
                user=request.user,
                fullname=serializer_obj.validated_data.get("fullname"),
                about=serializer_obj.validated_data.get("about")
            )
        except Exception as e:
            return Response(
                f"Database Error {e}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputProfileSerializer(profile).data)

    @extend_schema(responses=OutputProfileSerializer)
    def get(self, request):
        profile = get_profile(user=request.user)
        return Response(self.OutputProfileSerializer(profile).data)
