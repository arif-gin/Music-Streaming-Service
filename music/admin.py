from django.contrib import admin
from . models import Song, Favourites, History, Profile, EmailConfirmed

# Register your models here.


class EmailConfirmedAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'activation_key', 'email_confirmed']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

admin.site.register(EmailConfirmed, EmailConfirmedAdmin)


admin.site.register(Song)
admin.site.register(Favourites)
admin.site.register(History)
admin.site.register(Profile)

