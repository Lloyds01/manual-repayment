# Generated by Django 3.2.4 on 2022-03-16 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0009_loanrepayment_is_mandate_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrepayment',
            name='is_duplicate',
            field=models.BooleanField(default=False),
        ),
    ]
