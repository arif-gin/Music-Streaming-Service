from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib


class EmailConfirmed(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key=models.CharField(max_length=500)
    email_confirmed=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural='User Email-Confirmed'

@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirmed_instance=EmailConfirmed(user=instance)
        user_encoded=f'{instance.email}-{dt}'.encode()
        activation_key=hashlib.sha224(user_encoded).hexdigest()
        email_confirmed_instance.activation_key=activation_key
        email_confirmed_instance.save()


class Song(models.Model):
    song_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length= 50)
    singer = models.CharField(max_length= 50)
    language = models.CharField(max_length= 50,default='English')
    album = models.CharField(max_length= 50,default='')
    tags = models.CharField(max_length= 50)
    image = models.ImageField(upload_to = 'docs')
    song = models.FileField(upload_to= 'docs')
    movie = models.CharField(max_length = 50, default = "None")
    type = (
        ("Free", "Free"),
        ("Premium", "Premium"),
    )
    Song_Type = models.CharField(max_length=20, choices=type, default="Free")

    def __str__(self):
        return self.name


SUBSCRIPTION = (
    ('FREE' , 'FREE'),
    ('MONTHLY' , 'MONTHLY'),
    ('YEARLY' , 'YEARLY'),
    )

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    premium_Start_date = models.DateField(default=datetime.now(), null=True, blank=True)
    premium_expiry_date = models.DateField(null=True, blank=True)
    subscription_type = models.CharField(max_length=100 , choices=SUBSCRIPTION , default='FREE')

    def __str__(self):
        if self.is_premium is True:
            today = datetime.now().date()
            get_expired  = self.premium_expiry_date
            premium_valid_days = get_expired - today
            print(premium_valid_days.total_seconds())
            premium_valid_second = premium_valid_days.total_seconds()
            if premium_valid_second < 0:
                self.is_premium = False
                self.subscription_type = 'FREE'
                self.premium_Start_date = None
                self.premium_expiry_date = None
                self.save()

        return self.user.username + " - "+ str(self.is_premium)


class Favourites(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_id = models.CharField(max_length=10000000, default="")

class History(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music_id = models.CharField(max_length=10000000, default="")


