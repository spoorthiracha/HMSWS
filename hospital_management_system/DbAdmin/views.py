from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import mysql.connector as sqlc

from .forms import Add_FDOP_Form, Add_DEOP_Form, Add_Doctor_Form

host = "localhost"
port = "3306"
user = "vijay"
passwd = "Password@893"
database = "HMS"


def login_DbAdmin(request):    
    if request.method == "POST":
        # 203.110.242.34
        
        m = sqlc.connect(host="localhost",user="vijay",passwd="Password@893",database='HMS')
        cursor = m.cursor()
        d = request.POST
        for key,value in d.items():
            if key=="username":
                usr=value
            if key=="password":
                pwd=value
        query = "SELECT * FROM DbAdmin WHERE Username='{}' AND Password ='{}'".format(usr,pwd)
        cursor.execute(query)
        t = tuple(cursor.fetchall())
        print(t)

        if t ==():
            return render(request,'login_re.html')
        else:
            #return render(request,'datentry_dashboard.html')
            return HttpResponseRedirect('./administrator')
        m.close()
    return render(request,'login.html')


def action(request):
    template = loader.get_template('action.html')
    return HttpResponse(template.render());

def add_fdop(request):
    if request.method == 'POST':
        form = Add_FDOP_Form(request.POST)
        if form.is_valid():
            # Save the new front-desk operator to the database
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            # Do whatever you need to do with this data
            m = sqlc.connect(host=host, port=port, user=user, passwd=passwd, database=database)
            cursor = m.cursor()
            query = "INSERT INTO FrontDeskOp (Username, Password, Email, Name) VALUES ('{}', '{}', '{}', '{}')".format(username, password, email, name)
            cursor.execute(query)
            m.commit()
            return render(request, 'add_fdop.html', {'form': form})  # Replace 'dashboard' with the appropriate URL name
    else:
        form = Add_FDOP_Form()
    return render(request, 'add_fdop.html', {'form': form})

def add_deop(request):
    if request.method == 'POST':
        form = Add_DEOP_Form(request.POST)
        if form.is_valid():
            # Save the new front-desk operator to the database
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            # Do whatever you need to do with this data
            m = sqlc.connect(host=host, port=port, user=user, passwd=passwd, database=database)
            cursor = m.cursor()
            query = "INSERT INTO DataEntryOp (Username, Password, Email, Name) VALUES ('{}', '{}', '{}', '{}')".format(username, password, email, name)
            cursor.execute(query)
            m.commit()
            return render(request, 'add_deop.html', {'form': form})  # Replace 'dashboard' with the appropriate URL name
    else:
        form = Add_DEOP_Form()
    return render(request, 'add_deop.html', {'form': form})

def delete_fdop(request):
    # Retrieve the list of usernames from the database
    m = sqlc.connect(host=host, port=port, user=user, passwd=passwd, database=database)
    cursor = m.cursor()
    d = request.POST
    query = "SELECT Username FROM FrontDeskOp ORDER BY Username ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    usernames = [row[0] for row in rows]
    # Pass the list of usernames to the template
    context = {'usernames': usernames}

    if request.method == "POST":
        # Retrieve the username from the form
        username = request.POST['username']
        # Delete the user from the database
        query = "DELETE FROM FrontDeskOp WHERE Username='{}'".format(username)
        cursor.execute(query)
        m.commit()
        # Retrieve the updated list of usernames from the database
        query = "SELECT Username FROM FrontDeskOp ORDER BY Username ASC"
        cursor.execute(query)
        rows = cursor.fetchall()
        usernames = [row[0] for row in rows]
        # Pass the updated list of usernames to the template
        context = {'usernames': usernames}
    return render(request, 'delete_fdop.html', context)

def delete_deop(request):
    # Retrieve the list of usernames from the database
    m = sqlc.connect(host=host, port=port, user=user, passwd=passwd, database=database)
    cursor = m.cursor()
    d = request.POST
    query = "SELECT Username FROM DataEntryOp ORDER BY Username ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    usernames = [row[0] for row in rows]
    # Pass the list of usernames to the template
    context = {'usernames': usernames}

    if request.method == "POST":
        # Retrieve the username from the form
        username = request.POST['username']
        # Delete the user from the database
        query = "DELETE FROM DataEntryOp WHERE Username='{}'".format(username)
        cursor.execute(query)
        m.commit()
        # Retrieve the updated list of usernames from the database
        query = "SELECT Username FROM DataEntryOp ORDER BY Username ASC"
        cursor.execute(query)
        rows = cursor.fetchall()
        usernames = [row[0] for row in rows]
        # Pass the updated list of usernames to the template
        context = {'usernames': usernames}
    return render(request, 'delete_deop.html', context)

def add_doc(request):
    if request.method == 'POST':
        form = Add_Doctor_Form(request.POST)
        if form.is_valid():
            # Save the new front-desk operator to the database
            # employee_id = form.cleaned_data['employee_id']
            name = form.cleaned_data['name']
            department = form.cleaned_data['department']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            # Do whatever you need to do with this data
            m = sqlc.connect(host=host, port=port, user=user, passwd=passwd, database=database)
            cursor = m.cursor()
            query = "SELECT MAX(EmployeeID) FROM Doctor"
            cursor.execute(query)
            rows = cursor.fetchall()
            employee_id = rows[0][0] + 1
            working = 1
            query = "INSERT INTO Doctor (EmployeeID, Name, Department, Email, Phone, Password, Working) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(employee_id, name, department, email, phone, password, working)
            cursor.execute(query)
            m.commit()
            # return render(request, 'add_doc.html', {'form': form})  # Replace 'dashboard' with the appropriate URL name
    form = Add_Doctor_Form()
    return render(request, 'add_doc.html', {'form': form})

def delete_doc(request):
    # Retrieve the list of usernames from the database
    m = sqlc.connect(host=host, port=port, user=user, passwd=passwd, database=database)
    cursor = m.cursor()
    d = request.POST
    query = "SELECT * FROM Doctor WHERE Working=1 ORDER BY EmployeeID ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    context = {'rows': rows}

    if request.method == "POST":
        # Retrieve the username from the form
        employee_id = request.POST['employee_id']
        # Delete the user from the database
        query = "UPDATE Doctor SET Working=0 WHERE EmployeeID='{}'".format(employee_id)
        cursor.execute(query)
        m.commit()
        # Retrieve the updated list of usernames from the database
        query = "SELECT * FROM Doctor WHERE Working=1 ORDER BY EmployeeID ASC"
        cursor.execute(query)
        rows = cursor.fetchall
        context = {'rows': rows}
    return render(request, 'delete_doc.html', context)