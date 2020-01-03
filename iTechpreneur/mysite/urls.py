from django.urls import path

from .views import *



app_name = 'mysite'

urlpatterns = [
	path('',Home.as_view(),name='home'),

	

	path('student_registration/',Student_Registration.as_view(),name='student_registration'),
	
	# Graduate registration is specified in Future_Registration View 
	path('graduate_registration/',Future_Registration.as_view(),name='graduate_registration'),
	path('teacher_registration/',Teacher_Registration.as_view(),name='teacher_registration'),
	path('employee_registration/',Employee.as_view(),name='employee_registration'),
	path('existing_employee_registration/',ExistingEmployeeRegistration.as_view(),name='existing_employee_registration'),
	#Enterpreneurs Registration is used for Professor 
	path('professor_registration/',Entrepreneurs.as_view(),name='professor_registration'),
	path('login/',Login.as_view(),name='login'),
	path('logout/',Logout.as_view(),name='logout'),
	path('forgot/',ForgotPassword.as_view(),name='forgot'),
	path('profile/',Profile.as_view(),name='profile'),
	# path('student-dashboard/',StudentDashboard.as_view(),name='student-dashboard'),


#Graduate 
	path('future-dashboard/',FutureDashboard.as_view(),name='future-dashboard'),
	path('future-profile/',FutureProfile.as_view(),name='future-profile'),
	path('future-explore/', GraduateExplore.as_view(), name ='future-explore'),
	path('future-edit-profile/',FutureEditProfile.as_view(),name='future-edit-profile'),
	path('future-search-program/',FutureSearchProgram.as_view(),name='future-search-program'),
	path('future-academics-search/',Future_Search_Result.as_view(),name='future-academics-search'),
	path('future-notification/',FutureNotification.as_view(),name='future-notification'),
	path('future_teacher_create_notification/<int:id1>/<int:id2>/',future_teacher_create_notification, name='future_teacher_create_notification'),
	path('future_teacher_accept_notification/<int:id1>/<int:id2>/',future_teacher_accept_notification, name='future_teacher_accept_notification'),
	path('future_teacher_delete_notification/<int:id1>/',future_teacher_delete_notification, name='delete-notification'),
	path('future-teacher-following/',FutureTeacherFollowing.as_view(),name='future-teacher-following'),
	path('future-add-post/',FutureAddPost.as_view(),name='future-add-post'),
	path('future-group/',FutureGroupChat.as_view(),name='future-group'),
	path('future_teacher_unfollow/<int:id1>/<int:id2>/',future_teacher_unfollow,name='future_teacher_unfollow'),

#student
	path('existing-dashboard/',ExistingStudentDashboard.as_view(),name='existing-dashboard'),
	path('existing-profile/',ExistingStudentProfile.as_view(),name='existing-profile'),
	path('existing-notification/',ExistingStudentNotification.as_view(),name='existing-notification'),
	path('existing-search/',ExistingStudentSearch.as_view(),name='existing-search'),
	path('existing-explore/', ExistingExplore.as_view(), name ='existing-explore'),
	path('existing-following-employee/',ExistingStudentFollowingEmployees.as_view(),name='existing-following-employee'),
	path('existing-add-post/',ExistingStudentAddPost.as_view(),name='existing-add-post'),



#Professsor 
	path('teacher-dashboard/',TeacherDashboard.as_view(),name='teacher-dashboard'),
	path('teacher-profile/',TeacherProfile.as_view(),name='teacher-profile'),
	path('teacher-explore/', ProfessorExplore.as_view(), name ='teacher-explore'),
	path('teacher-search-future/',TeacherSearchFuture.as_view(),name='teacher-search-future'),
	path('teacher-search-exist/',TeacherSearchExist.as_view(),name='teacher-search-exist'),
	path('teacher-add-post/',TeacherAddPost.as_view(),name='teacher-add-post'),
	path('teacher-edit-post/',TeacherEditPost.as_view(),name='teacher-edit-post'),
	path('teacher-notification/',TeacherNotification.as_view(),name='teacher-notification'),
	# path('future-unfollow-by-teacher/<int:id1>/<int:id2>/',future_unfollow_by_teacher,name='future-unfollow-by-teacher'),

#employee 
	path('employee-dashboard/',EmployeeDashboard.as_view(),name='employee-dashboard'),
	path('employee-profile/',EmployeeProfile.as_view(),name='employee-profile'),
	path('employee-notification/',EmployeeNotification.as_view(),name='employee-notification'),
	path('employee-search-student/',EmployeeSearchStudent.as_view(),name='employee-search-student'),
	path('employee-student-following/',EmployeeStudentFollowing.as_view(),name='employee-student-following'),
	path('employee-add-post/',EmployeeAddPost.as_view(),name='employee-add-post'),
	path('employee-student-notification/<int:id1>/<int:id2>/',student_employee_create_notification,name='employee-student-notification'),
	path('employee-student-delete-notification/<int:id1>/',student_employee_delete_notification,name='employee-student-delete-notification'),
	path('student_employee_accept_notification/<int:id1>/<int:id2>/',student_employee_accept_notification,name='student_employee_accept_notification'),
	path('student_employee_unfollow_notification/<int:id1>/<int:id2>/',student_employee_unfollow_notification,name='student_employee_unfollow_notification'),


	#path('existing-employee-dashboard/',ExistingEmployeeDashboard.as_view(),name='existing-employee-dashboard'),
	#path('existing-employee-profile/',ExistingEmployeeProfile.as_view(),name='existing-employee-profile'),
	#path('existing-employee-notification/',ExistingEmployeeNotification.as_view(),name='existing-employee-notification'),
	#path('existing-employee-add-post/',ExistingEmployeeAddPost.as_view(),name='existing-employee-add-post'),
	#path('existing-employee-search-student/',ExistingEmployeeSearchStudent.as_view(),name='existing-employee-add-post-search-student'),


	# path('employee-dashboard/',EmployeeDashboard.as_view(),name='employee-dashboard'),
	# path('entrepreneurs-dashboard/',EntrepreneursDashboard.as_view(),name='entrepreneurs-dashboard'),

]




