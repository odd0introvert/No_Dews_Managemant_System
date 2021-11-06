from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class":"rounded-sm block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner",
                "placeholder":"Roll Number"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"rounded-sm block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner",
                "placeholder":"******"
            }
        )
    )

class Search(forms.Form):
    username1 = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class":"w-full py-2 px-1 placeholder-indigo-400 outline-none placeholder-opacity-50",
                "placeholder":"Roll Number"
            }
        )
    )

class RemoveStudent(forms.Form):
    username2 = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class":"w-full py-2 px-1 placeholder-indigo-400 outline-none placeholder-opacity-50",
                "placeholder":"Roll Number"
            }
        )
    )

class UpdateStudent(forms.Form):
    name = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":"Someone@gmail.com"
            }
        )
    )

    address = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "type":"date",
            }
        )
    )

    phone = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )
    father = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )

    nationality = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )
    religion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )

    caste = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )

    purpose = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "placeholder":""
            }
        )
    )

    Admission_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "type":"date",
            }
        )
    )

    Leaving_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class":"h-10 border mt-1 rounded px-4 w-full bg-gray-50",
                "type":"date",
            }
        )
    )

class MakeRequest(forms.Form):
    confirmation = forms.BooleanField(
        widget= forms.CheckboxInput(
            attrs={
                "type":"hidden"
            }
        )
    )

class Viewstudent(forms.Form):
    viewstd = forms.CharField(label="viewstd")

class DeleteRequest(forms.Form):
    decline = forms.CharField(label="decline")

class ConfirmRequest(forms.Form):
    rollno = forms.CharField(label="rollno")
    dept = forms.CharField(label="dept")


    