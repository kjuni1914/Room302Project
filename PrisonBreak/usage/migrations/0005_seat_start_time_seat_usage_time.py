# Generated by Django 4.2.11 on 2024-06-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0004_seat_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seat',
            name='usage_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]