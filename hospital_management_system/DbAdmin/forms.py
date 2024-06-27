from django import forms

class Add_FDOP_Form(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    name = forms.CharField(max_length=30)

class Add_DEOP_Form(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    name = forms.CharField(max_length=30)

class Add_Doctor_Form(forms.Form):
    # employee_id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    department = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=13)
    password = forms.CharField(widget=forms.PasswordInput)
