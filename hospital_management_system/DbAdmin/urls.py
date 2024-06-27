from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login', views.login_DbAdmin, name='login'),
    path('administrator/', views.action, name='action'),
    path('administrator/add_fdop', views.add_fdop, name='add_fdop'),
    path('administrator/add_deop', views.add_deop, name='add_deop'),
    path('administrator/add_doc', views.add_doc, name='add_doc'),
    path('administrator/delete_doc', views.delete_doc, name='delete_doc'),
    path('administrator/delete_fdop', views.delete_fdop, name='delete_fdop'),
    path('administrator/delete_deop', views.delete_deop, name='delete_deop'),
]
