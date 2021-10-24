from django.shortcuts import redirect, render
from .forms import LoginForm, AddStudent, MakeRequest, RemoveStudent, UpdateStudent
from django.contrib.auth import authenticate, login, logout
from .models import User, Staff, Student, Requests
from django.contrib.auth.hashers import make_password

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
            elif Student.objects.filter(Roll_No=username).exists() :
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
        return redirect('index')

def staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        form1 = AddStudent(request.POST or None)
        form2 = RemoveStudent(request.POST or None)
        staff = Staff.objects.get(Name=request.user.username)
        Reqs = Requests.objects.filter(Class=staff.Dept, Dept=False).values()
        students = Student.objects.filter(Dept=staff.Dept).values()
        if request.method == 'POST':
            if form1.is_valid():
                username1 = form1.cleaned_data.get('username1')
                add = Student(Roll_No=username1, Dept=staff.Dept)
                add.save()
        if request.method == "POST":
            if form2.is_valid():
                username2 = form2.cleaned_data.get('username2')
                remove = Student.objects.get(Roll_No=username2, Dept=staff.Dept)
                remove.delete()
        return render(request,'Staff_home.html', {'staff':staff, 'students':students, 'reqs':Reqs, 'form1':form1, 'form2':form2})
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
                student.Email = form1.cleaned_data.get('email')
                student.Address = form1.cleaned_data.get('address')
                student.DOB = form1.cleaned_data.get('dob')
                student.Phone = form1.cleaned_data.get('phone')
                student.Father_Name = form1.cleaned_data.get('father')
                student.Nationality = form1.cleaned_data.get('nationality')
                student.Religion = form1.cleaned_data.get('religion')
                student.Caste_Community = form1.cleaned_data.get('caste')
                student.save()

            if form2:
                print("request made")
                makereq = Requests(Roll_No = student.Roll_No, Class = student.Dept)
                makereq.save()
                return redirect('student')

        return render(request,'Student_home.html', {'student':student, 'req':Req, 'form1':form1, 'form2':form2})
    else:
        return redirect('index')

def signout(request):
    logout(request)
    return redirect('index')
    