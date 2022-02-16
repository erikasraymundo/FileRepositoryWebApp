from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name='index'),
    path('login/', views.loginView, name='loginView'),
    path('login/<int:error>', views.loginView, name='loginViewInvalid'),
    path('login/verification', views.login, name='login'),
    path('registration', views.registerView, name='registerView'),
    path('registration/verification', views.register, name='register'),
    path('logout', views.logout, name='logout')
]
