# Generated by Django 3.2.4 on 2022-03-15 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0007_rename_remita_manadate_loanrepayment_remita_mandate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanrepayment',
            old_name='remita_mandate',
            new_name='remita_mandate_id',
        ),
    ]
