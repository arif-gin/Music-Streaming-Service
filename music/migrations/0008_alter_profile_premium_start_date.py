# Generated by Django 3.2.9 on 2021-12-18 08:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20211216_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='premium_Start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 12, 18, 14, 54, 2, 282214), null=True),
        ),
    ]