from dataclasses import field, fields
from django.contrib import admin
from gateway.models import Jwt, LoanRepayment
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(Jwt)

@admin.register(LoanRepayment)
class RepaymentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'phone','amount','remita_id','payment_method','is_approved','payment_date',"entry_date"]

    search_fields = ['phone']

   