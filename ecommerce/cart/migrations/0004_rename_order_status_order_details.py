# Generated by Django 5.1.1 on 2024-10-22 04:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_payment'),
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order_status',
            new_name='Order_details',
        ),
    ]
