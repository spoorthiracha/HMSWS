from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', views.login_Doctor, name='login'),
    path('<str:usr>/home/', views.doctors, name='doctors'),
]
