from os import stat
from django.db import models
# from gateway.serializers import RepaymentSerializer
from repayment.models import CustomUser
from rest_framework.response import Response

# Create your models here.

class Jwt(models.Model):
    user = models.OneToOneField(CustomUser, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LoanRepayment(models.Model):

    choice=(

        ('TRANSFER','Transfer'),
        ('BANK DEPOSIT','Bank Deposit'),
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('OTHER', 'Other')

    )

    user                = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True )
    phone               = models.CharField(max_length=20, null=True, blank=True)
    amount              = models.CharField(max_length=50)
    remita_mandate     = models.CharField(max_length=50, null=True, blank=True)
    payment_date        = models.DateTimeField()
    entry_date          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    is_approved         = models.BooleanField(default=False)
    is_flagged         = models.BooleanField(default=False)
    payment_method      = models.CharField(max_length=30, choices=choice, default=choice[0][0])

    # @staticmethod
    # def check_repayment(request):
    #     if request.method == "POST":
    #         serializer = RepaymentSerializer(data = request.data)
    #         serializer.is_valid(raise_exception=True)

    #         payment_date = serializer.validated_data["payment_date"]
    #         amount = serializer.validated_data["amount"]
    #         remita_manadate = serializer.validated_data["remita_manadate"]
    #         is_flagged = (serializer.validated_data["is_flagged"])
    #         payment = LoanRepayment.objects.filter(payment_date=payment_date, amount=amount, remita_manadate=remita_manadate).exists()
    #         if payment:
    #             is_flagged == "True"
    #             response = ({'message':'This repayment exist already would you like to proceed'})
    #             return response
        

    def __str__(self):
        return self.phone

class Merge(models.Model):
    payment_id              = models.CharField(max_length=225)
    email                   = models.EmailField(unique=True)
    is_staff                = models.BooleanField()
    is_approved             = models.BooleanField()
    is_approved_all         = models.BooleanField()