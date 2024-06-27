from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.template import loader
import mysql.connector 
from django.views.decorators.csrf import csrf_exempt

usr=''
pwd=''

def login_FrontDeskOp(request):    
    if request.method == "POST":
        # 203.110.242.34
        
        m = mysql.connector.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
        print("HI3")
        cursor = m.cursor()
        d = request.POST
        for key,value in d.items():
            if key=="username":
                usr=value
            if key=="password":
                pwd=value
        query = "SELECT * FROM FrontDeskOp WHERE Username='{}' AND Password ='{}'".format(usr,pwd)
        cursor.execute(query)
        t = tuple(cursor.fetchall())
        print(t)

        if t ==():
            return render(request,'login_re.html')
        else:
            # return render(request,'_dashboard.html')
            return HttpResponseRedirect('../frontdeskop')
        m.close()
    return render(request,'login.html')


def frontdeskop(request):
  template = loader.get_template('frontdeskoperator.html')
  return HttpResponse(template.render())

def patient_reg(request):
   if request.method == "POST":
    # Connect to the database
    cnx = mysql.connector.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
    cursor = cnx.cursor()
    d = request.POST
    query="INSERT INTO Patient(Name, Gender, Age, Phone, Diagnosis) VALUES (%s, %s, %s, %s, %s);"
    try:
     cursor.execute(query,(str(d['name']),str(d['gender']),int(d['age']),str(d['phone']),str(d['diagnosis']),))
     cnx.commit()
    except mysql.connector.Error as err:
      if err !='':
        return HttpResponse (err.msg)

    # Close the database connection
    cursor.close()
    cnx.close()   
    return render(request, 'patient_reg.html')

   return render(request, 'patient_reg.html')
 
def patient_dis(request):
   if request.method == "POST":
    # Connect to the database
    cnx = mysql.connector.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
    cursor = cnx.cursor()
    data = request.POST
    query1="UPDATE Room SET Available = 1 WHERE Number IN (SELECT Room FROM Stay WHERE Patient = %s);"
    cursor.execute(query1,(str(data['pid']),))
    query2="DELETE FROM Stay WHERE Patient = %s;"
    cursor.execute(query2,(str(data['pid']),))
    cnx.commit()
    # Close the database connection
    cursor.close()
    cnx.close() 
    return render(request, 'patient_dis.html')
   return render(request, 'patient_dis.html')

@csrf_exempt
def doctor_appt(request):
  template = loader.get_template('doctor_appt.html')
  # Connect to the database
  cnx = mysql.connector.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
  cursor = cnx.cursor()

  if request.method == "POST":
    data = request.POST
    if 'did' in data:
     query1="SELECT Doctor, StartTime FROM Slots WHERE Available = 1 and Doctor = %s;"
     cursor.execute(query1, (int(data['did']),))
     slot_list = tuple(cursor.fetchall())
     context = {
        'slot_list': slot_list,
     }
    if 'pid' in data:
      query2="INSERT INTO Appointment(Doctor, Patient, Date, StartTime) VALUES(%s, %s, %s, %s);"
      try:
        cursor.execute(query2,(int(data['did_final']),int(data['pid']),str(data['apptdate']),str(data['appttime']),))
      except mysql.connector.Error as err:
        if err !='':
          return HttpResponse (err.msg)
      
      query3="UPDATE Slots SET Available = 0 WHERE Doctor = %s and StartTime = %s;"
      cursor.execute(query3,(int(data['did_final']),str(data['appttime']),))
      context = {
          'slot_list': [],
      }
      cnx.commit()

      q_apptid="SELECT AppointmentID FROM Appointment WHERE Doctor = %s and Patient = %s and Date = %s "
      cursor.execute(q_apptid,(int(data['did_final']),int(data['pid']),str(data['apptdate'])))
      apptid=(cursor.fetchall())
      print(apptid[0])
     #####insertion into Prescribes_Medication , Prescribes_Test , Prescribes_Treatment tables
      q4 = "INSERT INTO Prescribes_Medication(Doctor, Patient, Appointment,Medication) VALUES(%s, %s, %s, %s);"
      q5= "INSERT INTO Prescribes_Test(Doctor, Patient, Appointment,Date,Test,Results) VALUES(%s, %s, %s, %s, %s,%s);"
      q6= "INSERT INTO Prescribes_Treatment(Doctor, Patient, Appointment,Date,Treatment) VALUES(%s, %s, %s, %s,%s);"

      # cursor.execute(q4,(int(data['did_final']),int(data['pid']),int(apptid[0][0]),"None",))
      cursor.execute(q5,(int(data['did_final']),int(data['pid']),int(apptid[0][0]),str(data['apptdate']),"None","None",))
      cursor.execute(q6,(int(data['did_final']),int(data['pid']),int(apptid[0][0]),str(data['apptdate']),"None"))
      cnx.commit()  
    return HttpResponse(template.render(context, request))
  # Close the database connection
  


  cursor.close()
  cnx.close() 
  return HttpResponse(template.render())

def assign_room(request):
  template = loader.get_template('assign_room.html')
  # Connect to the database
  cnx = mysql.connector.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
  cursor = cnx.cursor()
  query1="SELECT Number, Type FROM Room WHERE Available = 1;"
  cursor.execute(query1)
  room_list = tuple(cursor.fetchall())
  context = {
        'room_list': room_list,
  }
  if request.method == "POST":
    data = request.POST
    query2="INSERT INTO Stay(Patient, Room) VALUES(%s, %s);"
    cursor.execute(query2,(int(data['pid']),int(data['roomnum']),))
    query3="UPDATE Room SET Available = 0 WHERE Number = %s and Type <> 'General Ward';"
    cursor.execute(query3,(int(data['roomnum']),))
    query4="SELECT Number, Type FROM Room WHERE Available = 1;"
    cursor.execute(query4)
    room_list = tuple(cursor.fetchall())
    context = {
        'room_list': room_list,
    }
    cnx.commit()  
    return HttpResponse(template.render(context, request))
  # Close the database connection
  cursor.close()
  cnx.close() 
  return HttpResponse(template.render(context, request))

@csrf_exempt
def test_scheduling(request):
  template = loader.get_template('test_scheduling.html')
  # Connect to the database
  cnx = mysql.connector.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
  cursor = cnx.cursor()
  if request.method == "POST":
    data = request.POST
    if 'testname' in data:
     query1="SELECT Test, StartTime FROM SlotsforTests WHERE Available = 1 and Test = %s;"
     cursor.execute(query1, (str(data['testname']),))
     slot_list = tuple(cursor.fetchall())
     context = {
        'slot_list': slot_list,
     }
    if 'pid' in data:
     query2="INSERT INTO Scheduled_Tests VALUES(%s, %s, %s, %s);"
     try:
      cursor.execute(query2,(int(data['pid']),str(data['testname_final']),str(data['testdate']),str(data['testtime']),))
     except mysql.connector.Error as err:
      if err !='':
        return HttpResponse (err.msg)
      
     query3="UPDATE SlotsforTests SET Available = 0 WHERE Test = %s and StartTime = %s;"
     cursor.execute(query3,(str(data['testname_final']),str(data['testtime']),))
     context = {
        'slot_list': [],
     }
    cnx.commit()  
    return HttpResponse(template.render(context, request))
  # Close the database connection
  cursor.close()
  cnx.close() 
  return HttpResponse(template.render())

@csrf_exempt
def treatment_scheduling(request):
  template = loader.get_template('treatment_scheduling.html')
  # Connect to the database
  cnx = mysql.connector.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
  cursor = cnx.cursor()
  if request.method == "POST":
    data = request.POST
    if 'treatmentname' in data:
     query1="SELECT Treatment, StartTime FROM SlotsforTreatments WHERE Available = 1 and Treatment = %s;"
     cursor.execute(query1, (str(data['treatmentname']),))
     slot_list = tuple(cursor.fetchall())
     context = {
        'slot_list': slot_list,
     }
    if 'pid' in data:
     query2="INSERT INTO Scheduled_Treatments VALUES(%s, %s, %s, %s);"
     try:
      cursor.execute(query2,(int(data['pid']),str(data['treatmentname_final']),str(data['treatmentdate']),str(data['treatmenttime']),))
     except mysql.connector.Error as err:
      if err !='':
        return HttpResponse (err.msg)
     query3="UPDATE SlotsforTreatments SET Available = 0 WHERE Treatment = %s and StartTime = %s;"
     cursor.execute(query3,(str(data['treatmentname_final']),str(data['treatmenttime']),))
     context = {
         'slot_list': [],
     }
     cnx.commit()  
    return HttpResponse(template.render(context, request))
  # Close the database connection
  cursor.close()
  cnx.close() 
  return HttpResponse(template.render())