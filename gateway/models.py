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
    remita_mandate_id   = models.CharField(max_length=50, null=True, blank=True)
    payment_date        = models.DateTimeField()
    entry_date          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    is_approved         = models.BooleanField(default=False)
    is_flagged          = models.BooleanField(default=False)
    payment_method      = models.CharField(max_length=30, choices=choice, default=choice[0][0])
    is_mandate_closed   = models.BooleanField(default=False)


    
    def __str__(self):
        return self.phone

    def flag_repayment(payment_date, amount, remita_mandate_id):
        
        payment = LoanRepayment.objects.filter(payment_date=payment_date, amount=amount, remita_mandate_id=remita_mandate_id)
        
        print(f'Loan Repayment: {payment}')
        if payment.exists():
            is_flagged = True
            print(f'is flagged value passed: {is_flagged}')
            result = payment.update(is_flagged = is_flagged)
            print(f'update query result: {result}')
            try:
                result < 1
            except:
                result = payment.update(is_flagged = is_flagged)
            else:
                response = ({'message':'This repayment exist already would you like to proceed'})
        return response

class Merge(models.Model):
    payment_id              = models.CharField(max_length=225)
    email                   = models.EmailField(unique=True)
    is_staff                = models.BooleanField()
    is_approved             = models.BooleanField()
    is_approved_all         = models.BooleanField()