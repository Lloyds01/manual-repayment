# Generated by Django 3.2.4 on 2022-03-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0003_alter_merge_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merge',
            name='payment_id',
            field=models.CharField(max_length=225),
        ),
    ]