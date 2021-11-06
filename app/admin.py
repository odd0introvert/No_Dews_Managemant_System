from django.contrib import admin
from .models import User, Student, Staff, Requests, Library, LAB, Hostel, Office

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Requests)
admin.site.register(Library)
admin.site.register(LAB)
admin.site.register(Hostel)
admin.site.register(Office)