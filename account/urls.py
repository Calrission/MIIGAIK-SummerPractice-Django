from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),

    # change password urls
    path('password-change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # reset password urls
    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
