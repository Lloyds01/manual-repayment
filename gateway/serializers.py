from dataclasses import field
from hashlib import new
from pyexpat import model
from gateway.models import LoanRepayment, Merge
from rest_framework import serializers
from repayment.models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()
   
class ResfreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = ["id", "phone", "amount","remita_id", "payment_date","payment_method"]

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class ApproveoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merge
        fields = ["payment_id", "email", "is_staff","is_approved"]

class ApproveallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merge
        fields = ["email", "is_staff","is_approved_all"]














# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

# class ResfreshSerializer(serializers.Serializer):
#     refresh = serializers.CharField()


# class RegisterSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
    