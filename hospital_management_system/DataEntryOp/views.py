from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
from django.template import loader
import mysql.connector as sqlc
from datetime import *

usr=''
pwd=''

def login_DataEntryOp(request):    
    if request.method == "POST":
        # 203.110.242.34
        
        m = sqlc.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
        print("HI3")
        cursor = m.cursor()
        d = request.POST
        for key,value in d.items():
            if key=="username":
                usr=value
            if key=="password":
                pwd=value
        query = "SELECT * FROM DataEntryOp WHERE Username='{}' AND Password ='{}'".format(usr,pwd)
        cursor.execute(query)
        t = tuple(cursor.fetchall())
        print(t)

        if t ==():
            return render(request,'login_re.html')
        else:
            # return render(request,'datentry_dashboard.html')
            return HttpResponseRedirect('../findpatient')
        m.close()
    return render(request,'login.html')




def findpatient(request):
    if request.method == "POST":
        m = sqlc.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
        cursor = m.cursor()
        d = request.POST
        patient_id = int()
        appid = int()
        action = ""
        for key, value in d.items():
            if key == 'patient_id':
                patient_id = value
            if key == 'appid':
                appid = value
            if key == 'action':
                action = value
        query = "SELECT * FROM Appointment WHERE Patient=%s AND AppointmentID=%s;"
        cursor.execute(query, (str(patient_id), str(appid),))
        context = {'patient_id': patient_id, 'appid': appid}
        t = tuple(cursor.fetchall())
        print("==========================")
        print(action)
        print("==========================")
        if t == ():
            return render(request, 'deopbase/findpatient.html')
        elif action == 'addTreatment':
            redirecturl = "../" + str(patient_id) + "/" + str(appid) + "/showTreatment"
            return HttpResponseRedirect(redirecturl, context)
        elif action == 'addTest':
            redirecturl = "../" + str(patient_id) + "/" + str(appid) + "/addTest"
            return HttpResponseRedirect(redirecturl, context)
        elif action == 'addAdministeredTreatment':
            redirecturl = "../" + str(patient_id) + "/" + str(appid) + "/addAdmTreatment"
            return HttpResponseRedirect(redirecturl, context)
        else:
            return render(request, 'deopbase/findpatient.html')
    return render(request, 'deopbase/findpatient.html')


def admTreatments(request, *args, **kwargs):
    patient_id = kwargs['patient_id']
    appid = kwargs['appid']
    context = {'patient_id': patient_id, 'appid': appid}
    m = sqlc.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
    cursor = m.cursor()
    if request.method == "POST":
        d = request.POST
        t_type = str()
        for key, value in d.items():
            if key == 't_type':
                t_type = value
        # CREATE TABLE AdministeredTreatments (Patient int NOT NULL,AppointmentID int NOT NULL,Treatment varchar(255) NOT NULL,PRIMARY KEY(Patient,Appointment,Treatment),FORIEGN KEY (Patient) REFERENCES Patient(PatientID),FORIEGN KEY (Appointment) REFERENCES Appointment(AppointmentID));
        query = "INSERT INTO AdministeredTreatments VALUES(%s,%s,%s)"
        cursor.execute(query, (patient_id, appid, t_type,))
        m.commit()
    return render(request, 'deopbase/addTreatment.html', context)


def updateTests(request, *args, **kwargs):
    patient_id = kwargs['patient_id']
    appid = kwargs['appid']
    context = {'patient_id': patient_id, 'appid': appid}
    m = sqlc.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
    cursor = m.cursor()
    query = "SELECT * FROM Appointment WHERE AppointmentID=%s AND Patient=%s;"
    cursor.execute(query, (appid, patient_id,))
    tuples = tuple(cursor.fetchall())
    doctor = tuples[0][1]
    query = "SELECT * FROM Prescribes_Test WHERE Doctor=%s AND Patient=%s AND Appointment=%s;"
    cursor.execute(query, (str(doctor), str(patient_id), str(appid),))
    context['tests'] = tuple(cursor.fetchall())
    if request.method == "POST":
        d = request.POST
        t_type = str()
        t_result = str()
        for key, value in d.items():
            # if key == 'patient_id':
            #
            #     #print(value)
            # if key == 'appid':
            #     appid = value
            if key == 'test_type':
                t_type = value
            if key == 'test_result':
                t_result = value
        # print("===========================")
        # print(patient_id)
        # print(appid)
        # print(t_type)
        # print(t_result)
        # print(tuples)
        # print("2")

        # print(doctor)
        # if t_type == "":
        #     # print("lamda")
        #     query = "SELECT * FROM Prescribes_Test WHERE Appointment=%s AND Patient=%s;"
        #     cursor.execute(query, (appid, patient_id,))
        #     t = tuple(cursor.fetchall())
        #     context['tests'] = t
        #     print(t)
        # if t != ():
        #     return render(request, 'deopbase/randomTest.html', context)

        # elif t_result == "":
        #     query = "INSERT INTO Prescribes_Test(Doctor,Patient,Appointment,Date,Test,Results) VALUES(%s,%s,%s,%s,%s,NULL)"
        #     cursor.execute(query, (str(doctor), str(patient_id), str(appid), str(date.today()), t_type,))
        #     query = "SELECT * FROM Prescribes_Treatment WHERE Patient=%s AND Appointment=%s;"
        #     cursor.execute(query, (str(patient_id), str(appid),))
        #     context['tests'] = tuple(cursor.fetchall())
        #     return HttpResponseRedirect('../addTests')

        # else:
        #     query = "INSERT INTO Prescribes_Test VALUES(%s,%s,%s,%s,%s,%s)"
        #     cursor.execute(query,
        #                    (str(doctor), str(patient_id), str(appid), str(date.today()), t_type, t_result,))
        #     query = "SELECT * FROM Prescribes_Test WHERE Doctor=%s AND Patient=%s AND Appointment=%s;"
        #     cursor.execute(query, (str(doctor), str(patient_id), str(appid),))
        #     context['tests'] = tuple(cursor.fetchall())
        #     return HttpResponseRedirect('../addTests')
        # else:  # query = "UPDATE Prescribes_Test SET Result=%s WHERE Appointment=%s AND Patient=%s AND Treatment=%s;"
        #     cursor.execute(query, (t_result, appid, patient_id, t_type,))
        query = "UPDATE Prescribes_Test SET Results=%s WHERE Appointment=%s AND Patient=%s AND Test=%s;"
        cursor.execute(query, (t_result, appid, patient_id, t_type,))
        m.commit()
        query = "SELECT * FROM Prescribes_Test WHERE Doctor=%s AND Patient=%s AND Appointment=%s;"
        cursor.execute(query, (str(doctor), str(patient_id), str(appid),))
        context['tests'] = tuple(cursor.fetchall())
    return render(request, 'deopbase/randomTest.html', context)


def updateTreatments(request, *arg, **kwargs):
    patient_id = kwargs['patient_id']
    appid = kwargs['appid']
    m = sqlc.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
    cursor = m.cursor()
    d = request.POST
    query = "SELECT * FROM Appointment WHERE AppointmentID=%s AND Patient=%s;"
    cursor.execute(query, (str(appid), str(patient_id),))
    context = {'patient_id': patient_id, 'appid': appid}
    tuples = tuple(cursor.fetchall())
    query = "SELECT * FROM AdministeredTreatments WHERE Patient=%s AND Appointment=%s;"
    cursor.execute(query, (patient_id, appid,))
    t = tuple(cursor.fetchall())
    context['treatments'] = t

    # print("++++++++")
    # print(patient_id)

    if tuples == ():
        return render(request, 'deopbase/randomTreatment.html')
    if request.method == "POST":
        t_type = str()
        for key, value in d.items():
            if key == 't_type':
                t_type = value
        query = "SELECT * FROM AdministeredTreatments WHERE Patient=%s AND Appointment=%s AND Treatment=%s"
        cursor.execute(query,(patient_id,appid,t_type,))
        rand=cursor.fetchall()
        if rand==():
            query = "INSERT INTO AdministeredTreatments VALUES(%s,%s,%s);"
            cursor.execute(query,(patient_id,appid,t_type,))
            m.commit()
            query = "SELECT * FROM AdministeredTreatments WHERE Patient=%s AND Appointment=%s;"
            cursor.execute(query, (patient_id, appid,))
            t = tuple(cursor.fetchall())

                #tuples = []
                # today = date.today()
                # timenow = datetime.now()
                # index = 0
                # for item in t:
                #     if item[2] < today or (item[2] == today and item[3] <= timenow + timedelta(hours=2)):
                #         tuples[index] = item
                #         index = index + 1

            context['treatments'] = t
    return render(request, 'deopbase/randomTreatment.html', context)