from django.db import models

# Create your models here.
class Students (models.Model):

    Roll_No = models.CharField(max_length=20)
    Reg_No = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    Name = models.CharField(max_length=30)
    DOB = models.DateField()
    Dept = models.CharField(max_length=20)
    Email = models.EmailField()
    Father_Name = models.CharField(max_length=20)
    Address = models.CharField(max_length=100)
    Nationality = models.CharField(max_length=15)
    Religion = models.CharField(max_length=10)
    Caste_Community = models.CharField(max_length=5)
    Scholarship = models.BooleanField()
    Date_Of_Admission = models.DateField()
    Date_Of_Leaving = models.DateField()
    Purpose_Of_TC = models.CharField(max_length=50)
    No_Dues_Certificate = models.BooleanField()
    Conduct = models.CharField(max_length=10)
    Signature_Of_HOD = models.BooleanField()
    Due_Department = models.BooleanField()
    Due_Library = models.BooleanField()
    Due_PE = models.BooleanField()
    Due_NSS = models.BooleanField()
    Due_Hostel = models.BooleanField()
    Due_Office = models.BooleanField()
    Due_Labs = models.BooleanField()

    def __str__(self):
        return self.Roll_No
        
class Staffs (models.Model):
    
    Name = models.CharField(max_length=30)
    Password = models.CharField(max_length=20)
    Email = models.EmailField()
    Dept = models.CharField(max_length=20)
    
    def __str__(self):
        return self.Name