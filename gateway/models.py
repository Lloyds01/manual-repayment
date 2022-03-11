from django.db import models
from repayment.models import CustomUser

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
    remita_id           = models.CharField(max_length=50, null=True, blank=True)
    payment_date        = models.DateTimeField()
    entry_date          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    is_approved         = models.BooleanField(default=False)
    payment_method      = models.CharField(max_length=30, choices=choice, default=choice[0][0])

    def __str__(self):
        return self.phone

class Merge(models.Model):
    payment_id              = models.CharField(max_length=225)
    email                   = models.EmailField(unique=True)
    is_staff                = models.BooleanField()
    is_approved             = models.BooleanField()
    is_approved_all         = models.BooleanField()