from django.urls import path
from . import views 

urlpatterns = [
	path('',views.index, name='index'),
	path('staff/login',views.stafflogin, name='stafflogin'),
	path('staff/',views.staff, name='staff'),
	path('student/login',views.studentlogin, name='studentlogin'),
	path('student/',views.student, name='student'),
	path('admin/login',views.adminlogin, name='adminlogin'),
	path('admin/',views.admin, name='admin'),
	path('logout/',views.signout, name='logout'),
]