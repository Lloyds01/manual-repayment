from dataclasses import field, fields
from django.contrib import admin
from gateway.models import Csv, Jwt, LoanRepayment
from import_export.admin import ImportExportModelAdmin


# Register your models here.

admin.site.register(Jwt)
admin.site.register(Csv)

@admin.register(LoanRepayment)
class RepaymentAdmin(ImportExportModelAdmin):
    list_display = ['user', 'id', 'phone', 'amount', 'remita_mandate_id', 'payment_method', 'is_flagged', 'is_approved',
                    'payment_date', "entry_date", "is_mandate_closed", "is_duplicate", "internal", "external", "branch_name", "repayment_posted"]

    search_fields = ['phone']
