# Generated by Django 3.2.6 on 2021-12-16 16:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0006_alter_profile_premium_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='premium_Start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 12, 16, 22, 57, 0, 887855), null=True),
        ),
        migrations.CreateModel(
            name='EmailConfirmed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(max_length=500)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Email-Confirmed',
            },
        ),
    ]
