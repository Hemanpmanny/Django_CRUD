from django.shortcuts import render,redirect
from django.views import View
from .models import Students
from .forms import *

# Create your views here.

class Home(View):
    
    def get(self,request):
        stu_data=Students.objects.all()
        return render(request,'home.html',{'students':stu_data})
    
    
class AddStudents(View):
    def get(self,request):
        fm=AddStudentsForm()
        return render(request,'add_students.html',{'form':fm})
    
    def post(self,request):
        fm=AddStudentsForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('/')
        else:
            return render(request,'add_students.html',{'form':fm})
        
class DeleteStudent(View):
     def post(self,request):
         data=request.POST
         id=data.get('id')
         student=Students.objects.get(id=id)
         student.delete()
         return redirect('/')
     
class UpdateStudent(View):
    def get(self,request,id):
        stu=Students.objects.get(id=id)
        fm=AddStudentsForm(instance=stu)
        return render(request,'update_student.html',{'form':fm})
    
    def post(self,request,id):
        stu=Students.objects.get(id=id)
        fm=AddStudentsForm(request.POST,instance=stu)
        
        if fm.is_valid():
            fm.save()
            return redirect('/')
        
        else:
            return render(request,'update_student.html',{'form':fm})
        
        
    
         
    
