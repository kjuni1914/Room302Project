# Generated by Django 4.2.11 on 2024-06-03 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0010_remove_seat_estimated_using_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='usage_type',
            field=models.CharField(choices=[('Personal', 'Personal'), ('Team', 'Team')], default='Personal', max_length=10),
        ),
        migrations.AlterField(
            model_name='seat',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]