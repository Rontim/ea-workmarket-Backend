# Generated by Django 4.2.3 on 2023-07-11 20:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_alter_jobbids_date_of_bidding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobbids',
            name='date_of_bidding',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
