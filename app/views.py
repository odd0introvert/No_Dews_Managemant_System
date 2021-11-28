from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from app.models import User, Staff, Student, Requests, Due
from app.forms import AdminLogin, StaffLogin, StudentLogin
from django.core import serializers
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def stafflogin(request):
    form = StaffLogin(request.POST or None)
    msg = None
    year = None
    if request.method == 'POST':
        if form.is_valid():
            Department = form.cleaned_data.get('Department')
            password = form.cleaned_data.get('Password')
            year = form.cleaned_data.get('Year')
            user = authenticate(username=Department, password=password, Year=year)
            
            if Staff.objects.filter(Dept=Department,Year=year).exists():
                if user is not None and user.is_staff:
                    login(request, user)
                    return redirect('staff')
                elif User.objects.filter(username=Department, Year=year).exists():
                    msg='Invalid Credentials'
                else:
                    create = User(username=Department, password=make_password(password), is_staff = True, Year=year)
                    create.save()
                    msg='User Created, Please login to continue'
                    return render(request, 'staff-login.html',{'form':form,'msg':msg})
            else:
                msg='Something went Wrong'
            
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('student')         
    elif request.user.is_authenticated and request.user.is_admin:
        return redirect('admin')                              
    else:            
        return render(request, 'staff-login.html',{'form':form,'msg':msg})

def studentlogin(request):   
    form = StudentLogin(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            regno = form.cleaned_data.get('Register_Number')
            password = form.cleaned_data.get('Password')
            user = authenticate(username=regno, password=password)
            if Student.objects.filter(Reg_No=regno).exists():
                if user is not None and user.is_student:
                    login(request, user)
                    return redirect('student')
                elif User.objects.filter(username=regno).exists():
                    msg='Invalid Credentials'
                else:
                    create = User(username=regno, password=make_password(password), is_student = True)
                    create.save()
                    msg='User Created, Please login to continue'
                    return render(request, 'student-login.html',{'form':form,'msg':msg})
            else:
                msg='Something went Wrong'

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('student')         
    elif request.user.is_authenticated and request.user.is_admin:
        return redirect('admin')                      
    else:
        return render(request, 'student-login.html', {'form':form,'msg':msg})

def adminlogin(request):
    form = AdminLogin(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('Username')
            password = form.cleaned_data.get('Password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('admin')
            elif User.objects.filter(username=username).exists():
                msg='Invalid Credentials'
            else:
                create = User(username=username, password=make_password(password), is_admin = True)
                create.save()
                msg='User Created, Please login to continue'
                return render(request, 'admin-login.html',{'form':form,'msg':msg})
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('student')         
    elif request.user.is_authenticated and request.user.is_admin:
        return redirect('admin')
    else:        
        return render(request, 'admin-login.html', {'form':form,'msg':msg})

def signout(request):
    logout(request)
    return redirect('/')

def sendemail(regno,email,context,subject):
    message = f'Hello, ' + regno + ' ' + context
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )

def getdues(request):

    staff = Staff.objects.get(Dept=request.user.username)
    students = Student.objects.filter().values()

    if staff.Dept == "PG_Lab":
        dues = Due.objects.filter(Dept='PG_Lab')
    elif staff.Dept == "UG_Lab":
        dues = Due.objects.filter(Dept='UG_Lab')
    elif staff.Dept == "Hostel":
        dues = Due.objects.filter(Dept='Hostel')
    elif staff.Dept == "Library":
        dues = Due.objects.filter(Dept='Library')
    elif staff.Dept == "Office":
        dues = Due.objects.filter(Dept='Office')
    else:
        temp = list()
        for student in students:
            if student["Dept"] == staff.Dept:
                temp.append(student["Reg_No"])
        dues = Due.objects.filter(Reg_No__in=temp)

    return (dues)

def ajaxget(request):
    
    staff = Staff.objects.get(Dept=request.user.username)
    regno = request.GET.get('regno', None)
    search = request.GET.get('search', None)
    getmodeldata = request.GET.get('getmodeldata', None)
    getmodeldatadue = request.GET.get('getmodeldatadue', None)
    if getmodeldatadue == 'True':
        ReqDue = Due.objects.filter(Reg_No=regno).values()
        data = json.dumps(list(ReqDue), cls=DjangoJSONEncoder)
        return(data)
    if getmodeldata == 'True':
        ReqStudent = serializers.serialize('json', [ Student.objects.get(Reg_No=regno, Year=staff.Year), ])
        return(ReqStudent)
    if search == 'True':
        query = request.GET.get('query', None)
        search = serializers.serialize('json', [ Student.objects.get(Reg_No=query), ]) 
        return (search)

def ajaxpost(request):
    removedue = request.POST.get('removedue', None)
    acceptreq = request.POST.get('AcceptReq', None)
    adddue = request.POST.get('AddDue', None)
    if acceptreq == 'True':
        regno = request.POST.get('regno', None)
        print(regno)
        dept = request.POST.get('dept', None)
        accept = Requests.objects.get(Reg_No=regno)
        print(accept)
        if dept == "Library":
            accept.Library = '1'
        elif dept == "Hostel":
            accept.Hostel = '1'
        elif dept == "Office":
            accept.Office = '1'
            student = Student.objects.get(Reg_No = regno)
            email = student.Email
            sendemail(regno,email,'Your Verification process has been completed successfully, Please collect your Transfer certificate in the office room.','Verification process completed!')
        elif dept == "UG_Lab":
            accept.UG_Lab = '1'
        elif dept == "PG_Lab":
            accept.PG_Lab = '1'
        else:
            accept.Dept = '1'
        
        accept.save()
        return ('Accepted')
    if adddue == 'True':
        regno = request.POST.get('regno', None)
        dept = request.POST.get('dept', None)
        year = request.POST.get('year', None)
        status = request.POST.get('due', None)
        if status == 'True':
            status = '0'
        else:
            status = '1'
        if Due.objects.filter(Reg_No=regno, Dept=dept).exists():
            return('Already Exist') 
        else:
            add=Due(Reg_No = regno, Dept = dept, Year = year, is_Done = status)
            add.save()
            return ('Due added')
    if removedue == 'True':
        regno = request.POST.get('regno', None)
        dept = request.POST.get('dept', None)
        remove=Due.objects.get(Reg_No=regno, Dept=dept)
        remove.delete()
        return ('Due Removed')

def getreq(request):

    staff = Staff.objects.get(Dept=request.user.username)
    students = Student.objects.filter().values()

    temp = list()
    for student in students:
        if student["Dept"] == staff.Dept:
            temp.append(student["Reg_No"])

    if staff.Dept == "Library":
        reqs = Requests.objects.filter(Q(Dept='1', UG_Lab='1', Library='0') | Q(Dept='1', PG_Lab='1', Library='0'))
    elif staff.Dept == "Hostel":
        reqs = Requests.objects.filter(Q(Dept='1', Library='1', UG_Lab='1',  Hostel='0') | Q(Dept='1', Library='1', PG_Lab='1',  Hostel='0'))
    elif staff.Dept == "Office":
        reqs = Requests.objects.filter(Q(Dept='1', UG_Lab='1', Library='1', Hostel='1', Office='0') | Q(Dept='1', PG_Lab='1', Library='1', Hostel='1', Office='0'))
    elif staff.Dept == "UG_Lab":
        ug = list()
        for student in students:
            if student["Level"] == 'UG':
                ug.append(student["Reg_No"])
        reqs = Requests.objects.filter(Reg_No__in=ug,Dept='1',UG_Lab='0')
    elif staff.Dept == "PG_Lab":
        pg = list()
        for student in students:
            if student["Level"] == 'PG':
                pg.append(student["Reg_No"])
        reqs = Requests.objects.filter(Reg_No__in=pg,Dept='1',PG_Lab='0')
        for req in reqs:
            print(req.Reg_No)
    else:
        temp1 = list()
        for student in students:
            if student["Dept"] == staff.Dept:
                temp1.append(student["Reg_No"])
        reqs = Requests.objects.filter(Reg_No__in=temp1,Dept='0')

    return(reqs)

@login_required(login_url='/staff/login')

def staff(request):
    if request.user.is_staff:
        staff = Staff.objects.get(Dept=request.user.username)
        students = Student.objects.filter().values()

        temp = list()
        for student in students:
            if student["Dept"] == staff.Dept:
                print(student["Reg_No"])
                temp.append(student["Reg_No"])
        print(temp)
        dept_students = Student.objects.filter(Reg_No__in=temp)
        dues = getdues(request)
        reqs = getreq(request)
        
        if request.is_ajax and request.method == "GET":
            response = ajaxget(request)
            if response:
                return JsonResponse(response, safe=False , content_type="application/json")
            else:
                return render(request, 'staff-home.html',{'staff':staff,'deptstudents':dept_students,'students':students,'reqs':reqs,'dues':dues})
        if request.is_ajax and request.method == "POST":
            response = ajaxpost(request)
            return JsonResponse(response, safe=False , content_type="application/json")

        return render(request, 'staff-home.html',{'staff':staff,'deptstudents':dept_students,'students':students,'reqs':reqs,'dues':dues})

@login_required(login_url='/student/login')

def student(request):
    if request.user.is_student:
        student = Student.objects.get(Reg_No=request.user.username)
        if Requests.objects.filter(Reg_No=student.Reg_No).exists():
            req = Requests.objects.get(Reg_No=student.Reg_No) 
        else: 
            req = None  
        if request.is_ajax and request.method == "POST":
            purpose = request.POST.get('purpose', None)
            date_of_leaving = request.POST.get('date_of_leaving', None)
            if Requests.objects.filter(Reg_No=student.Reg_No).exists():
                return JsonResponse('Request already exist', safe=False, content_type="application/json")
            else:
                student.Purpose_Of_TC = purpose
                student.Date_Of_Leaving = date_of_leaving
                student.Applied = '1'
                create = Requests(Reg_No=student.Reg_No)
                student.save()
                create.save()
                emails = list()
                staffs = Staff.objects.filter().values()
                for staff in staffs:
                    if staff["Dept"] == 'PG_Lab' or staff["Dept"] == 'UG_Lab' or staff["Dept"] == 'Library' or staff["Dept"] == 'Hostel' or staff["Dept"] == 'Office' or staff["Dept"] == student.Dept:
                        emails.append(staff["Email"])
                for email in emails:
                    sendemail(student.Reg_No,email,'is requested for verification','Verification request!')
                return JsonResponse('Success', safe=False, content_type="application/json")
        else:
            print('hit normal')
            return render(request, 'student-home.html',{'student':student,'req':req})
        
@login_required(login_url='/admin/login')

def admin(request):
    if request.user.is_admin:
        students = Student.objects.filter().values()
        staffs = Staff.objects.filter().values()
        users = User.objects.filter().values()
        return render(request, 'admin-home.html',{'students':students,'staffs':staffs,'users':users})