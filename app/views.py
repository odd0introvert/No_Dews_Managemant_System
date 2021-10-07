from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import Students, Staffs

# Create your views here.
def Student_login(request):

    if not request.user.is_authenticated:
    
        if request.method == 'POST':

            rollno = str(request.POST.get('rollno'))
            password = str(request.POST.get('password'))
        
            try:

                Student_user = Students.objects.get(Roll_No=rollno,Password=password)

                if Student_user is not None:

                    Student_user = authenticate( username=rollno, password=password)

                    if Student_user is not None:
                        
                        Student_user = authenticate(request, username=rollno, password=password)
                        login(request,Student_user)
                        return redirect('/Student')

                    else:

                        Student_user = User.objects.create_user(username=rollno,password=password)
                        Student_user.save()
                        return redirect('/Student')

            except Exception as e:

                messages.info(request,"Invalid Credentials")
                return render(request, 'Student_login.html')
        else :

            return render(request, 'Student_login.html')

    else : 

        return redirect('/Student')

def Student_logout(request):
    
    logout(request)

    return redirect('/Student_login')

def Student_home(request):
    
    if not request.user.is_authenticated:

        return redirect('/Student_login')

    else:

        return render(request, 'Student_home.html')
        
def Staff_login(request):
    
    if not request.user.is_authenticated:
    
        if request.method == 'POST':

            name = str(request.POST.get('Name'))
            password = str(request.POST.get('password'))
        
            try:

                Staff_user = Staffs.objects.get(Name=name,Password=password)

                if Staff_user is not None:

                    Staff_user = authenticate( username=name, password=password)

                    if Staff_user is not None:
                        
                        Staff_user = authenticate(request, username=name, password=password)
                        login(request,Staff_user)
                        return redirect('/Staff')

                    else:

                        Staff_user = User.objects.create_user(username=name,password=password)
                        Staff_user.save()
                        return redirect('/Staff')

            except Exception as e:

                messages.info(request,e)
                return render(request, 'Staff_login.html')
        else :

            return render(request, 'Staff_login.html')

    else : 

        return redirect('/Staff')

def Staff_logout(request):
    
    logout(request)

    return redirect('/Staff_login')

def Staff_home(request):
    
    if not request.user.is_authenticated:

        return redirect('/Staff_login')

    else:

        return render(request, 'Staff_home.html')
        