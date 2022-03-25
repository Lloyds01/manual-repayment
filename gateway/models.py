import io
from os import stat
from django.db import models
from repayment.models import CustomUser
from rest_framework.response import Response
# import pandas as pd

# Create your models here.


class Jwt(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LoanRepayment(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    amount = models.FloatField(default=0.0)
    remita_mandate_id = models.CharField(max_length=50, null=True, blank=True)
    payment_date = models.DateTimeField()
    entry_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100, default="Transfer")
    is_mandate_closed = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    internal = models.BooleanField(default=False)
    external = models.BooleanField(default=False)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    repayment_posted = models.BooleanField(default=False)

    def __str__(self):
        return self.phone

    @property
    def username(self):
        return self.user.name

    @property
    def total_pending_approval(self):
        return LoanRepayment.objects.filter(is_approved=False).count()

    # @staticmethod
    # def process_repayment_from_csv(csv_file):

    #     file_data = csv_file.read()
    #     df = pd.read_csv(io.BytesIO(file_data), header=None,
    #                      usecols=[4], names=["contacts"], dtype="O")
    #     df["repayment"] = df["amount","payment_method","payment_date","remita_mandate_id","phone"].str[-10:]
        
        
    #     return dict(contacts = good_numbers["trimmed"].to_list(), errors = fixes_required, total_added = total_added)

    # @staticmethod
    # def add_contacts(group, numbers: list):

    #     contacts = map(lambda number: Contact(
    #         mobile_number=number, group_id=group), numbers)
    #     Contact.objects.bulk_create(contacts)

    #     return True



class Merge(models.Model):
    payment_id = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField()
    is_approved = models.BooleanField()
    is_approved_all = models.BooleanField()

class Csv(models.Model):
    file_name = models.FileField(upload_to="csvs")
    uploaded =models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name