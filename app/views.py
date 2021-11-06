from django.shortcuts import redirect, render
from .forms import ConfirmRequest, LoginForm, MakeRequest, RemoveStudent, Search, UpdateStudent, Viewstudent, DeleteRequest
from django.contrib.auth import authenticate, login, logout
from .models import User, Staff, Student, Requests, Library, LAB, Office, Hostel
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def index(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('student')
    else:
        form = LoginForm(request.POST or None)
        msg = None
        return render(request, 'login.html', {'form': form, 'msg': msg})

def signin(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_staff:
                login(request, user)
                return redirect('staff')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('student')
            elif Student.objects.filter(Roll_No=username.upper).exists() :
                create = User(username=username, password=make_password(password), is_student = True)
                create.save()
                msg= 'user created Please login'
            elif Staff.objects.filter(Name=username).exists():
                create = User(username=username, password=make_password(password), is_staff = True)
                create.save()
                msg= 'user created Please login'
            else:
                msg= 'invalid credentials'      
        else:
            msg = 'error validating form'

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('student')
    else:
        return render(request, 'login.html', {'form': form, 'msg': msg})

def admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'admin.html')
    else:
        return redirect('/admin')

def staff(request):
    if request.user.is_authenticated and request.user.is_staff: 
        form1 = Search(request.POST)
        form2 = RemoveStudent(request.POST)
        form3 = ConfirmRequest(request.POST)
        form4 = Viewstudent(request.POST)
        form5 = DeleteRequest(request.POST)
        staff = Staff.objects.get(Name=request.user.username)
        Reqs = Requests.objects.filter().values()
        students = Student.objects.filter(Dept=staff.Dept).values()
        dues = None
        search = None
        view = None

        if request.method == 'POST':
            if form1.is_valid():
                username1 = form1.cleaned_data.get('username1').upper()
                if Student.objects.filter(Roll_No=username1).exists():
                    search = Student.objects.get(Roll_No=username1)
                else :
                    search = None

        if request.method == "POST":
            if form2.is_valid():
                username2 = form2.cleaned_data.get('username2')
                remove = Student.objects.get(Roll_No=username2, Dept=staff.Dept)
                remove.delete()

        if request.method == "POST":
            if form3.is_valid():
                rollno = form3.cleaned_data.get('rollno')
                dept = form3.cleaned_data.get('dept')
                print(rollno)
                std = Student.objects.get(Roll_No=rollno)
                req = Requests.objects.get(Roll_No=rollno)
                if dept == "library":
                    std.Due_Library = True
                    req.Library = True
                elif dept == "hostel":
                    std.Due_Hostel = True
                    req.Hostel = True
                elif dept == "office":
                    std.Due_Office = True
                    req.Office = True
                    subject = 'Due Verification Completed!'
                    message = f'Hello, ' + std.Roll_No + ' your Due verification has been completed, Please collect your Tc in the office.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [std.Email, ]
                    send_mail( subject, message, email_from, recipient_list )
                elif dept == "lab":
                    std.Due_Labs = True
                    req.Labs = True
                else:
                    std.Due_Department = True
                    req.Dept = True

                std.save()
                req.save()

        if request.method == "POST":
            if form4.is_valid():
                rollno = form4.cleaned_data.get('viewstd')

                if Student.objects.filter(Roll_No=rollno).exists():
                    view = Student.objects.get(Roll_No=rollno)

                if staff.Dept == 'library':
                    dues = Library.objects.filter(Roll_No=rollno).values()
                elif staff.Dept == 'lab':
                    dues = LAB.objects.filter(Roll_No=rollno).values()
                elif staff.Dept == 'office':
                    dues = Office.objects.filter(Roll_No=rollno).values()
                elif staff.Dept == 'hostel':
                    dues = Hostel.objects.filter(Roll_No=rollno).values()
                else:
                    dues = None

        if request.method == "POST":
            if form5.is_valid():
                rollno = form5.cleaned_data.get('decline')

                if Requests.objects.filter(Roll_No=rollno).exists():
                    Requests.objects.filter(Roll_No=rollno).delete()

        return render(request,'Staff_home.html', {'dues':dues, 'view':view,'search':search,'staff':staff, 'students':students, 'reqs':Reqs, 'form1':form1, 'form2':form2, 'form3':form3, 'form4':form4})
    else:
        return redirect('index')

def student(request):
    if request.user.is_authenticated and request.user.is_student:
        form1 = UpdateStudent(request.POST or None)
        form2 = MakeRequest(request.POST or None)
        student = Student.objects.get(Roll_No=request.user.username)

        if Requests.objects.filter(Roll_No=request.user.username).exists():
            Req = Requests.objects.get(Roll_No=student.Roll_No)
        else : 
            Req = None
        
        if request.method == "POST":
            if form1.is_valid():
                student.Name = form1.cleaned_data.get('name')
                student.Reg_No = student.Roll_No
                student.Email = form1.cleaned_data.get('email')
                student.Address = form1.cleaned_data.get('address')
                student.DOB = form1.cleaned_data.get('dob')
                student.Phone = form1.cleaned_data.get('phone')
                student.Father_Name = form1.cleaned_data.get('father')
                student.Nationality = form1.cleaned_data.get('nationality')
                student.Religion = form1.cleaned_data.get('religion')
                student.Caste_Community = form1.cleaned_data.get('caste')
                student.Date_Of_Admission = form1.cleaned_data.get('Admission_date')
                student.Date_Of_Leaving = form1.cleaned_data.get('Leaving_date')
                student.Purpose_Of_TC = form1.cleaned_data.get('purpose')
                student.save()

            if form2:
                if not Requests.objects.filter(Roll_No=student.Roll_No).exists():
                    makereq = Requests(Roll_No = student.Roll_No, Class = student.Dept)
                    makereq.save()
                    student.applied = True
                    student.save()
                    staffs = Staff.objects.filter().values()
                    for staff in staffs:
                        dept = staff.get('Dept')
                        email = staff.get('Email')
                        if dept == student.Dept or dept == 'library' or dept == 'PE' or dept == 'NSS' or dept == 'Hostel' or dept == 'Office' :
                            subject = 'Dwe Verification Alert!'
                            message = f'Hello, ' + student.Roll_No + ' requested for Dwe verification.'
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [email, ]
                            send_mail( subject, message, email_from, recipient_list )
                            print('mail send to: ' + email)
                return redirect('student')

        return render(request,'Student_home.html', {'student':student, 'req':Req, 'form1':form1, 'form2':form2})
    else:
        return redirect('index')

def signout(request):
    logout(request)
    return redirect('index')
    