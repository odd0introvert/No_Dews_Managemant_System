from django.contrib import admin
from .models import User, Student, Staff, Requests

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Requests)