"""RyzicMix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from music import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from music.forms import MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm


admin.site.site_header = "RyzicMix"
admin.site.site_title = "RyzicMix Admin Panel"
admin.site.index_title = "RyzicMix Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('music/', include('music.urls')),
    path('signup', views.signup, name = "signup"),
    path('login/', views.login, name = "login"),

     # email activation
    path('email/confirmation/<str:activation_key>/', views.email_confirm, name='email_activation'),

    # Change Password
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='music/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchnagedone/'),name='passwordchange'),
    path('passwordchnagedone/',auth_views.PasswordChangeDoneView.as_view(template_name='music/passwordchangedone.html'),name='passwordchnagedone'),

    # password reset
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='music/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='music/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='music/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='music/password_reset_complete.html'),name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
