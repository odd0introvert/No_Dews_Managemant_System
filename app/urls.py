from django.urls import path
from . import views 

urlpatterns = [
	path('',views.Student_login, name='Student_login'),
    path('Student_login',views.Student_login, name='Student_login'),
    path('Student_logout',views.Student_logout, name='Student_logout'),
    path('Student',views.Student_home, name='Student_home'),
    path('Staff_login',views.Staff_login, name='Staff_login'),
    path('Staff_logout',views.Staff_logout, name='Staff_logout'),
    path('Staff',views.Staff_home, name='Staff_home'),
]
