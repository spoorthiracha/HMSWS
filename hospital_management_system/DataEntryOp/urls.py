from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', views.login_DataEntryOp, name='login'),
    path('findpatient/', views.findpatient, name="findpatient"),
    path('<str:patient_id>/<str:appid>/addTest/', views.updateTests, name="addTest"),
    path('<str:patient_id>/<str:appid>/showTreatment/', views.updateTreatments, name="addTreatment"),
    path('<str:patient_id>/<str:appid>/addAdmTreatment/', views.admTreatments, name="admTreatment"),
]
