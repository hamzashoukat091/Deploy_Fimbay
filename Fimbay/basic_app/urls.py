from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    path('login/',views.login, name='login'),
    path('signup/',views.register, name='register'),
]
