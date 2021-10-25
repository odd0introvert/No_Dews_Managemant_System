from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_staff = models.BooleanField('Is staff', default=False)
    is_student = models.BooleanField('Is student', default=False)

class Student (models.Model):
    
    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Reg_No = models.CharField(max_length=20, default=None, null=True)
    Name = models.CharField(max_length=30, default=None, null=True)
    DOB = models.DateField(default=None, null=True)
    Phone = models.CharField(max_length=10, default=None, null=True)
    Dept = models.CharField(max_length=20, default=None, null=True)
    Email = models.EmailField(default=None, null=True)
    Father_Name = models.CharField(max_length=20, default=None, null=True)
    Address = models.CharField(max_length=100, default=None, null=True)
    Nationality = models.CharField(max_length=15, default=None, null=True)
    Religion = models.CharField(max_length=10, default=None, null=True)
    Caste_Community = models.CharField(max_length=5, default=None, null=True)
    Date_Of_Admission = models.DateField(default=None, null=True)
    Date_Of_Leaving = models.DateField(default=None, null=True)
    Purpose_Of_TC = models.CharField(max_length=50, default=None, null=True)
    Conduct = models.CharField(max_length=10, default=None, null=True)
    Due_Department = models.BooleanField(default=False, null=True)
    Due_Library = models.BooleanField(default=False, null=True)
    Due_PE = models.BooleanField(default=False, null=True)
    Due_NSS = models.BooleanField(default=False, null=True)
    Due_Hostel = models.BooleanField(default=False, null=True)
    Due_Office = models.BooleanField(default=False, null=True)
    Due_Labs = models.BooleanField(default=False, null=True)

        
class Staff (models.Model):
    
    Name = models.CharField(max_length=30, default=None, null=True)
    Email = models.EmailField(default=None, null=True)
    Dept = models.CharField(max_length=20, default=None, null=True)

class Requests (models.Model):

    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Class = models.CharField(max_length=20, default=None, null=True)
    Dept = models.BooleanField(default=False, null=True)
    Library = models.BooleanField(default=False, null=True)
    PE = models.BooleanField(default=False, null=True)
    NSS = models.BooleanField(default=False, null=True)
    Hostel = models.BooleanField(default=False, null=True)
    Office = models.BooleanField(default=False, null=True)
    Labs = models.BooleanField(default=False, null=True)