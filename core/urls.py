from django.urls import path
from .views import *

urlpatterns=[
    path('',Home.as_view(),name="home"),
    path('add_stu/',AddStudents.as_view(),name="add_stu"),
    path('delete_stu/',DeleteStudent.as_view(),name="delete_stu"),
    path('update_stu/<int:id>',UpdateStudent.as_view(),name="update_stu")
]