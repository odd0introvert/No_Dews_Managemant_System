from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_staff = models.BooleanField('Is staff', default=False)
    is_student = models.BooleanField('Is student', default=False)

class Student (models.Model):
    
    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Reg_No = models.CharField(max_length=20, default=None, null=True, blank=True)
    Name = models.CharField(max_length=30, default=None, null=True, blank=True)
    DOB = models.DateField(default=None, null=True, blank=True)
    Phone = models.CharField(max_length=10, default=None, null=True, blank=True)
    Dept = models.CharField(max_length=20, default=None, null=True, blank=True)
    Email = models.EmailField(default=None, null=True, blank=True)
    Father_Name = models.CharField(max_length=20, default=None, null=True, blank=True)
    Address = models.CharField(max_length=100, default=None, null=True, blank=True)
    Nationality = models.CharField(max_length=15, default=None, null=True, blank=True)
    Religion = models.CharField(max_length=10, default=None, null=True, blank=True)
    Caste_Community = models.CharField(max_length=5, default=None, null=True, blank=True)
    Date_Of_Admission = models.DateField(default=None, null=True, blank=True)
    Date_Of_Leaving = models.DateField(default=None, null=True, blank=True)
    Purpose_Of_TC = models.CharField(max_length=50, default=None, null=True, blank=True)
    Conduct = models.CharField(max_length=10, default=None, null=True, blank=True)
    Due_Department = models.BooleanField(default=False, null=True, blank=True)
    Due_Library = models.BooleanField(default=False, null=True, blank=True)
    Due_Hostel = models.BooleanField(default=False, null=True, blank=True)
    Due_Office = models.BooleanField(default=False, null=True, blank=True)
    Due_Labs = models.BooleanField(default=False, null=True, blank=True)
    Applied = models.BooleanField(default=False, null=True, blank=True)

        
class Staff (models.Model):
    
    Name = models.CharField(max_length=30, default=None, null=True)
    Email = models.EmailField(default=None, null=True, blank=True)
    Dept = models.CharField(max_length=20, default=None, null=True, blank=True)

class Requests (models.Model):

    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Class = models.CharField(max_length=20, default=None, null=True, blank=True)
    Dept = models.BooleanField(default=False, null=True, blank=True)
    Library = models.BooleanField(default=False, null=True, blank=True)
    Hostel = models.BooleanField(default=False, null=True, blank=True)
    Office = models.BooleanField(default=False, null=True, blank=True)
    Labs = models.BooleanField(default=False, null=True, blank=True)

class Library (models.Model):

    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Book = models.CharField(max_length=20, default=None, null=True, blank=True)
    Initial_Date = models.DateField(default=None, null=True, blank=True)
    Due_Date = models.DateField(default=None, null=True, blank=True)
    is_Returened = models.BooleanField(default=False, null=True, blank=True)

class LAB (models.Model):
    
    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Instrument = models.CharField(max_length=20, default=None, null=True, blank=True)
    Due_Date = models.DateField(default=None, null=True, blank=True)
    is_Paid = models.BooleanField(default=False, null=True, blank=True)

class Office (models.Model):
    
    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Type = models.CharField(max_length=20, default=None, null=True, blank=True)
    Due_Date = models.DateField(default=None, null=True, blank=True)
    is_Paid = models.BooleanField(default=False, null=True, blank=True)

class Hostel (models.Model):
    
    Roll_No = models.CharField(max_length=20, default=None, null=True)
    Fees = models.CharField(max_length=20, default=None, null=True, blank=True)
    Due_Date = models.DateField(default=None, null=True, blank=True)
    is_Paid = models.BooleanField(default=False, null=True, blank=True)
