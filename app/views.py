from django.shortcuts import redirect, render
from .forms import ConfirmRequest, LoginForm, AddStudent, MakeRequest, RemoveStudent, UpdateStudent
from django.contrib.auth import authenticate, login, logout
from .models import User, Staff, Student, Requests
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from reportlab.pdfgen import canvas

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
        return redirect('/admin')

def staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        form1 = AddStudent(request.POST)
        form2 = RemoveStudent(request.POST)
        form3 = ConfirmRequest(request.POST)
        staff = Staff.objects.get(Name=request.user.username)
        Reqs = Requests.objects.filter(Class=staff.Dept).values()
        students = Student.objects.filter(Dept=staff.Dept).values()
        if request.method == 'POST':
            if form1.is_valid():
                username1 = form1.cleaned_data.get('username1')
                conduct = form1.cleaned_data.get('conduct')
                add = Student(Roll_No=username1, Dept=staff.Dept, Conduct=conduct)
                add.save()
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
                elif dept == "pe":
                    std.Due_PE = True
                    req.PE = True
                elif dept == "nss":
                    std.Due_NSS = True
                    req.NSS = True
                elif dept == "hostel":
                    std.Due_Hostel = True
                    req.Hostel = True
                elif dept == "office":
                    std.Due_Office = True
                    req.Office = True
                elif dept == "lab":
                    std.Due_Labs = True
                    req.Labs = True
                else:
                    std.Due_Department = True
                    req.Dept = True

                std.save()
                req.save()

        return render(request,'Staff_home.html', {'staff':staff, 'students':students, 'reqs':Reqs, 'form1':form1, 'form2':form2, 'form3':form3})
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
                print("request made")
                makereq = Requests(Roll_No = student.Roll_No, Class = student.Dept)
                makereq.save()
                return redirect('student')

        return render(request,'Student_home.html', {'student':student, 'req':Req, 'form1':form1, 'form2':form2})
    else:
        return redirect('index')

def pdf(request):

    if request.user.is_authenticated and request.user.is_student:

        student = Student.objects.get(Roll_No=request.user.username)
        # Create the HttpResponse object 
        response = HttpResponse(content_type='application/pdf') 

        p = canvas.Canvas(response)

        # Write content on the PDF 
        p.drawString(250, 700, "College Tc Generation") 
        p.drawString(100, 650, "Name: " + student.Name)
        p.drawString(100, 625, "Roll Number: " + student.Roll_No)
        p.drawString(100, 600, "Register Number: " + student.Reg_No)
        p.drawString(100, 575, "Date of birth: " + str(student.DOB))
        p.drawString(100, 550, "Department: " + student.Dept)
        p.drawString(100, 525, "Address : " + student.Address)
        p.drawString(100, 500, "Phone : " + student.Phone)
        p.drawString(100, 475, "Email : " + student.Email) 
        p.drawString(100, 450, "Father Name: " + student.Father_Name)
        p.drawString(100, 425, "Nationality : " + student.Nationality)
        p.drawString(100, 400, "Religion  : " + student.Religion)
        p.drawString(100, 375, "Caste/Community  : " + student.Caste_Community) 
        p.drawString(100, 350, "Conduct : " + student.Conduct) 
        p.drawString(100, 325, "Date of Admission: " + str(student.Date_Of_Admission))
        p.drawString(100, 300, "Date of Leaving : " + str(student.Date_Of_Leaving))
        p.drawString(100, 275, "Purpose of TC : " + student.Purpose_Of_TC)
        p.drawString(400, 225, "HOD Signature")

        # Close the PDF object. 
        p.showPage() 
        p.save() 

        # Show the result to the user    
        return response
    else:
        return redirect('index')

def signout(request):
    logout(request)
    return redirect('index')
    