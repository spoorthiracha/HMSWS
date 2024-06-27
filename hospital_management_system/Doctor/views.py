from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.template import loader
from django.core.files import File
import mysql.connector as sqlc
from hospital_management_system.settings import XMLFILES_FOLDER

path = XMLFILES_FOLDER+'Doctor/doctor_login.txt'


usr=''
pwd=''

def login_Doctor(request):    
    if request.method == "POST":        
        m = sqlc.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
        cursor = m.cursor()
        d = request.POST
        for key,value in d.items():
            if key=="username":
                usr=value
            if key=="password":
                pwd=value
        query = "SELECT * FROM Doctor WHERE EmployeeID='{}' AND Password ='{}'".format(usr,pwd)
        cursor.execute(query)
        t = tuple(cursor.fetchall())
        print(t)

        if t ==():
            return render(request,'login_re.html')
        else:
            # return render(request,'doctor_dashboard.html')

            f = open(path, 'w')
            testfile = File(f)
            testfile.write(usr)
            testfile.close
            f.close
            redirecturl = "../" + str(usr) +"/home"
            return HttpResponseRedirect(redirecturl)
    return render(request,'login.html')




def doctors(request,*args,**kwargs):
    user = kwargs["usr"]
    # print("----------------------------------------------------")
    # f = open(path, 'r')
    # if f.mode == 'r':
    #     usr =f.read()
    # f.close
    # print(usr)
    m = sqlc.connect(host="127.0.0.1", user="vijay", passwd="Password@893", database='HMS')
    cursor = m.cursor()
    query = "SELECT Name FROM Doctor WHERE EmployeeID='{}';".format(user)
    cursor.execute(query)
    name=tuple(cursor.fetchall())
    
    
    query1 = "SELECT DISTINCT PatientID,Name,Gender,Age,Diagnosis FROM Patient LEFT JOIN Appointment ON Patient.PatientID = Appointment.Patient LEFT JOIN Prescribes_Medication ON Patient.PatientID = Prescribes_Medication.Patient LEFT JOIN Prescribes_Treatment ON Patient.PatientID = Prescribes_Treatment.Patient LEFT JOIN Prescribes_Test ON Patient.PatientID = Prescribes_Test.Patient WHERE Appointment.Doctor = '{}';".format(user)
    template = loader.get_template('doctor_dashboard.html')
    cursor.execute(query1)
    patient_list = tuple(cursor.fetchall())

    
    
    
    context = {
        'patient_list': patient_list,
        'name': name,
        'usr': user,
        'usr_image':'doctor_images/'+user+'.jpg',
    }
    if request.method == "POST":
        d = request.POST
        pid = 0
        pid_med = 0
        med = ''
        treatment = ''
        test = ''
        appointmentid = ''
        for key, value in d.items():
            if key == "patient-id":
                pid = value
            if key == "patient-id-Medicine":
                pid_med = value
            if key == "Medicine":
                med = value
            if key == "Treatment":
                treatment = value
            if key == "Test":
                test = value
            if key == "appointmentid":
                appointmentid = value
        if pid_med == 0:
            query2 = "SELECT  * FROM Patient LEFT JOIN Appointment ON Patient.PatientID = Appointment.Patient LEFT JOIN Prescribes_Medication ON Patient.PatientID = Prescribes_Medication.Patient LEFT JOIN Prescribes_Treatment ON Patient.PatientID = Prescribes_Treatment.Patient LEFT JOIN Prescribes_Test ON Patient.PatientID = Prescribes_Test.Patient WHERE Appointment.Doctor = '{}' AND Appointment.Patient = '{} ';".format(user,pid)
            cursor.execute(query2)
            patient_info = tuple(cursor.fetchall())
            context = {
                'patient_list': patient_list,
                'name': name,
        	    'usr': user,
                'usr_image':'doctor_images/'+user+'.jpg',
                'patient_info': patient_info,
            }
        else:
            query_update_med = "UPDATE Prescribes_Medication SET Medication = '{}' WHERE Doctor='{}' AND Patient='{}' AND Appointment='{}'".format(med,user, pid_med,appointmentid)
            query_update_treatment = "UPDATE Prescribes_Treatment SET Treatment = '{}' WHERE Doctor='{}' AND Patient='{}' AND Appointment='{}'".format(treatment,user, pid_med,appointmentid)
            query_update_test = "UPDATE Prescribes_Test SET Test = '{}' WHERE Doctor='{}' AND Patient='{}' AND Appointment='{}'".format(test,user, pid_med, appointmentid)
            # print(query_update_med)
            if med != '':
                cursor.execute(query_update_med)
                m.commit()
            if treatment != '':
                cursor.execute(query_update_treatment)
                m.commit()
            if test != '':
                cursor.execute(query_update_test)
                m.commit()

    m.close()

    return HttpResponse(template.render(context, request))
