# Generated by Django 3.2.9 on 2021-11-30 07:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20211130_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='premium_Start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 30, 13, 15, 49, 555278), null=True),
        ),
    ]
