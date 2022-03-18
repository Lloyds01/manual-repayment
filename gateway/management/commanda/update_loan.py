from django.core.management.base import BaseCommand
from gateway.models import LoanRepayment
import requests


class Command(BaseCommand):
    help = "FETCH ALL APPROVED PAYMENTS AND CHECK WITH MAIN USSD LOAN DB AND KNOW THE MANDATE STATUS FOR THE REPAYMWNT"

    def handle(self, *args, **kwargs):
        url = "https://libertyussd.com/api/get_loan_data/"

        all_repayment = LoanRepayment.objects.filter(is_mandate_closed = False)

        if all_repayment:
            for payment in all_repayment:
                pass
            payload = {'mandate': '100632590264', 'phone': '07063185109'}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)
