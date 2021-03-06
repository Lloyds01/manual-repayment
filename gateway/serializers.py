from dataclasses import field
from xml.parsers.expat import model
from rest_framework.response import Response
from gateway.models import Csv, LoanRepayment, Merge
from rest_framework import serializers
from repayment.models import CustomUser
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class PostRepaymentSerializer(serializers.Serializer):
    phone = serializers.CharField()
    amount = serializers.FloatField()
    remita_mandate_id = serializers.CharField()
    payment_method = serializers.CharField()
    payment_date = serializers.CharField()


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = ["username", "id", "phone", "amount",
                  "remita_mandate_id", "payment_date", "payment_method"]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ApproveoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merge
        fields = ["payment_id", "email", "is_staff", "is_approved"]


class ApproveallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merge
        fields = ["email", "is_staff", "is_approved_all"]


class ConfirmRepaymentSerializer(serializers.Serializer):
    phone = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class UpdateAprrovedPaymentSerializer(serializers.Serializer):
    mandate = serializers.CharField()
    phone = serializers.CharField()


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ("file",)
