# Generated by Django 3.2.4 on 2022-03-16 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0010_loanrepayment_is_duplicate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrepayment',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]