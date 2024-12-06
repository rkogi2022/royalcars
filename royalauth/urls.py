from django.urls import path

from royalauth import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('PasswordResetSent/', views.PasswordResetSent, name='PasswordResetSent'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('LogoutView/', views.LogoutView, name='LogoutView'),
]