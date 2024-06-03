from django.shortcuts import render
from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    # Registration and verification
    path('register/', views.register_user, name='register'),
    path('email-verification/', lambda request: render(request, 'account/email/email_verification_sent.html'), name='email-verification-sent'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_user, name='profile'),
    path('delete-user/', views.delete_user, name='delete-user')

    # path()
]
