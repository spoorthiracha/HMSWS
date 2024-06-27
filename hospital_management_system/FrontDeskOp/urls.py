from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', views.login_FrontDeskOp, name='login'),
    path('frontdeskop/', views.frontdeskop, name='frontdeskop'),
    path('frontdeskop/patient_reg.html', views.patient_reg, name='patient_reg'),
    path('frontdeskop/patient_dis.html', views.patient_dis, name='patient_dis'),
    path('frontdeskop/doctor_appt.html', views.doctor_appt, name='doctor_appt'),
    path('frontdeskop/assign_room.html', views.assign_room, name='assign_room'),
    path('frontdeskop/test_scheduling.html', views.test_scheduling, name='test_scheduling'),
    path('frontdeskop/treatment_scheduling.html', views.treatment_scheduling, name='treatment_scheduling'),
]

