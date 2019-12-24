from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Employeeee)
admin.site.register(Professor)
admin.site.register(Graduate)
admin.site.register(StudentType)
admin.site.register(TechnicalSubject)
#admin.site.register(Subjects)
#admin.site.register(Skills)
#admin.site.register(Industry)
admin.site.register(Country)
#admin.site.register(UserType)
#admin.site.register(Future_Student)
admin.site.register(Students)
#admin.site.register(User_Info)
#admin.site.register(Teacher)
#admin.site.register(Position)
#admin.site.register(Title)
#admin.site.register(TeacherFutureNotifications)
#admin.site.register(Teacher_connections)
#admin.site.register(Future_connections)
#admin.site.register(ExistingEmployee)
#admin.site.register(StudentEmployeeNotification)
#admin.site.register(StudentEmployeeMapping)
#admin.site.register(EmployeeStudentMapping)

#Teacher Model will be used as Professor posts
admin.site.register(Teacher_post)
# Graduate Posts will be saved in Future Student Post
admin.site.register(Future_student_post)
admin.site.register(Employee_post)
admin.site.register(Existing_student_post)
#admin.site.register(TeacherStudentNotification)
#admin.site.register(FutureTeacherMapping)
#admin.site.register(TeacherFutureMapping)
