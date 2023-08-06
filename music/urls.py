from django.urls import path 
from . import views

from django.contrib.auth import views as auth_views
from .forms import MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm


urlpatterns = [
    path('songs/', views.songs, name = 'songs'),
    path('songs/<int:id>', views.songpost, name = 'songpost'),
    # path('login', views.login, name = "login"),
    path('logout_user', views.logout_user, name = "logout_user"),
    path('favourites', views.favourites, name = "favourites"),
    path('history', views.history, name = "history"),
    path('search',views.search,name='search'),
    path('subscription',views.subscription,name='subscription'),
    path('payment_page',views.payment_page,name='payment_page'),
    path('check_member',views.check_member,name='check_member'),
    path('remove_fav_song/<int:pk>',views.remove_fav_song,name='remove_fav_song'),
    path('cancel_membership',views.cancel_membership,name='cancel_membership'),
]