from django.urls import path
from . import views 

urlpatterns = [
	path('',views.signin, name='index'),
	path('login/',views.signin, name='login'),
	path('staff/',views.staff, name='staff'),
	path('student/',views.student, name='student'),
	path('logout',views.signout, name='logout'),
]