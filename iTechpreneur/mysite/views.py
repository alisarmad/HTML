from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login ,logout
from .models import *
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
import urllib.request
import json
from django.conf import settings
import smtplib
from smtplib import SMTPException
from email.message import EmailMessage
import os,random,string
import json
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.template.loader import get_template



def index(request):
	return render(request, 'mysite/chat.html', {})


class Home(TemplateView):
	template_name=('mysite/index.html')

def registration_done(request):
	render(request, 'registration_done.html')


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk = uid)
		#print("user :", user)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user and account_activation_token.check_token(user, token):
		user.is_active = True
		user.is_staff = True
		
		user.save()
		#print("user is activated", user)
		login(request, user)
		return redirect('mysite:login')
	else:
		return render(request, 'account_activation_invalid.html')


#ExistingExplore (List of all users)
class ExistingExplore(TemplateView):
	template_name = ('mysite/existing-dashboard/explore.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingExplore, self).get_context_data(*args, **kwargs)
		user_id = int(self.request.session['_auth_user_id'])
		

		#response_dict = {}
		response_list = []
		students = Students.objects.exclude(username_id = user_id)
		graduates = Graduate.objects.exclude(username_id = user_id)
		professors = Professor.objects.exclude(username_id = user_id)
		employees = Employeeee.objects.exclude(username_id = user_id)

		logged_user = Students.objects.filter(username_id = user_id).first()
		if logged_user is None:
			logged_user = Graduate.objects.filter(username_id = user_id).first()
		if logged_user is None:
			logged_user = Professor.objects.filter(username_id = user_id).first()
		if logged_user is None:
			logged_user = Employeeee.objects.filter(username_id = user_id).first()
		
		followers_objects = StudentFollowing.objects.all()
		#print("followers objects: ", followers_objects)


		#if followers_objects:
			#for i in followers_objects:
				#print("follower",i.follower_email)
				#print("following",i.following_email)
			
		
		if students:
			for i in students:
				#print("students .email :",i.email )
				context1 = {}
				#logged user id
				if followers_objects:
					for j in followers_objects:
						#print()
						if logged_user.email == j.follower_email and i.email == j.following_email:
							#print("j.follower email: ",logged_user, j.follower_email, i.email, j.following_email)
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if graduates:
			for i in graduates:
				context1 = {}
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				#logged user id 
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if professors:
			for i in professors:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if employees:
			for i in employees:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		#response_list.append(students)
		#response_list.append(graduates)
		#response_list.append(professors)
		#response_list.append(employees)
		#print("all users ",response_list)
		#response_dict.update(response_list)
		#print(response_dict)
		context['all_users'] = response_list
		return context
	def post(self, request):
		try:
			#print('in explore')
			#print('data', request.POST)
			follower_email = request.POST.get('follower_email')
			following_email = request.POST.get('following_email')
			#print('email: ', following_email)
			#print('user id', follower_email)
			#check record if it is exist
			
			status = StudentFollowing.objects.filter(following_email = following_email, follower_email = follower_email).first()
			#status1 = StudentFollowing.objects.filter(following_email = following_email, following_email = following_email).first()
			if status:
				status.delete()
				#print("status ", status)
				return HttpResponse('2')
			else:
				#print("could not found")
				follow_info = StudentFollowing.objects.create( following_email = following_email, follower_email = follower_email)
				follow_info.save()
				return HttpResponse('1')
		except Exception as e:
			#print('error ',e)
			return HttpResponse('3')

# Graduate Explore

#Explore (List of all users)
class GraduateExplore(TemplateView):
	template_name = ('mysite/future-dasboard/explore.html')
	def get_context_data(self, *args, **kwargs):
		context = super(GraduateExplore, self).get_context_data(*args, **kwargs)
		user_id = int(self.request.session['_auth_user_id'])
		

		#response_dict = {}
		response_list = []
		students = Students.objects.exclude(username_id = user_id)
		graduates = Graduate.objects.exclude(username_id = user_id)
		professors = Professor.objects.exclude(username_id = user_id)
		employees = Employeeee.objects.exclude(username_id = user_id)

		logged_user = Students.objects.filter(username_id = user_id).first()
		if logged_user is None:
			logged_user = Graduate.objects.filter(username_id = user_id).first()
		elif logged_user is None:
			logged_user = Professor.objects.filter(username_id = user_id).first()
		elif logged_user is None:
			logged_user = Employeeee.objects.filter(username_id = user_id).first()
		
		followers_objects = StudentFollowing.objects.all()
		#print("followers objects: ", followers_objects)


		
		if students:
			for i in students:
				#print("students .email :",i.email )
				context1 = {}
				#logged user id
				if followers_objects:
					for j in followers_objects:
						
						if logged_user.email == j.follower_email and i.email == j.following_email:
							
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if graduates:
			for i in graduates:
				context1 = {}
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				#logged user id 
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if professors:
			for i in professors:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if employees:
			for i in employees:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		#response_list.append(students)
		#response_list.append(graduates)
		#response_list.append(professors)
		#response_list.append(employees)
		#print("all users ",response_list)
		#response_dict.update(response_list)
		#print(response_dict)
		context['all_users'] = response_list
		return context
	def post(self, request):
		try:
			#print('in explore')
			#print('data', request.POST)
			follower_email = request.POST.get('follower_email')
			following_email = request.POST.get('following_email')
			#print('email: ', following_email)
			#print('user id', follower_email)
			#check record if it is exist
			
			status = StudentFollowing.objects.filter(following_email = following_email, follower_email = follower_email).first()
			#status1 = StudentFollowing.objects.filter(following_email = following_email, following_email = following_email).first()
			if status:
				status.delete()
				#print("status ", status)
				return HttpResponse('2')
			else:
				#print("could not found")
				follow_info = StudentFollowing.objects.create( following_email = following_email, follower_email = follower_email)
				follow_info.save()
				return HttpResponse('1')
		except Exception as e:
			#print('error ',e)
			return HttpResponse('3')


# Professor Explore
#Explore (List of all users)
class ProfessorExplore(TemplateView):
	template_name = ('mysite/teacher-dashboard/explore.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ProfessorExplore, self).get_context_data(*args, **kwargs)
		user_id = int(self.request.session['_auth_user_id'])
		#print("logged user id :", user_id)

		#response_dict = {}
		response_list = []
		students = Students.objects.exclude(username_id = user_id)
		graduates = Graduate.objects.exclude(username_id = user_id)
		professors = Professor.objects.exclude(username_id = user_id)
		employees = Employeeee.objects.exclude(username_id = user_id)

		logged_user = Students.objects.filter(username_id = user_id).first()
		#print("student logged :", logged_user)
		if logged_user is None:
			#print("logged graduate")
			logged_user = Graduate.objects.filter(username_id = user_id).first()
			#print("logged graduate:::", logged_user)
		if logged_user is None:
			logged_user = Professor.objects.filter(username_id = user_id).first()
			#print("logged user from professor: ", logged_user)
		if logged_user is None:
			#print("logged employee")
			logged_user = Employeeee.objects.filter(username_id = user_id).first()
		
		followers_objects = StudentFollowing.objects.all()
		#print("followers objects: ", followers_objects)



		if students:
			for i in students:
				#print("students .email :",i.email )
				context1 = {}
				#logged user id
				if followers_objects:
					for j in followers_objects:
						
						if logged_user.email == j.follower_email and i.email == j.following_email:
							
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if graduates:
			for i in graduates:
				context1 = {}
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				#logged user id 
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if professors:
			for i in professors:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if employees:
			for i in employees:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		#response_list.append(students)
		#response_list.append(graduates)
		#response_list.append(professors)
		#response_list.append(employees)
		#print("all users ",response_list)
		#response_dict.update(response_list)
		#print(response_dict)
		context['all_users'] = response_list
		return context
	def post(self, request):
		try:
			#print('in explore')
			#print('data', request.POST)
			follower_email = request.POST.get('follower_email')
			following_email = request.POST.get('following_email')
			#print('email: ', following_email)
			#print('user id', follower_email)
			#check record if it is exist
			
			status = StudentFollowing.objects.filter(following_email = following_email, follower_email = follower_email).first()
			#status1 = StudentFollowing.objects.filter(following_email = following_email, following_email = following_email).first()
			if status:
				status.delete()
				#print("status ", status)
				return HttpResponse('2')
			else:
				#print("could not found")
				follow_info = StudentFollowing.objects.create( following_email = following_email, follower_email = follower_email)
				follow_info.save()
				return HttpResponse('1')
		except Exception as e:
			#print('error ',e)
			return HttpResponse('3')


#Employee Explore
#Explore (List of all users)
class EmployeeExplore(TemplateView):
	template_name = ('mysite/employee-dashboard/explore.html')
	def get_context_data(self, *args, **kwargs):
		context = super(EmployeeExplore, self).get_context_data(*args, **kwargs)
		user_id = int(self.request.session['_auth_user_id'])
		

		#response_dict = {}
		response_list = []
		students = Students.objects.exclude(username_id = user_id)
		graduates = Graduate.objects.exclude(username_id = user_id)
		professors = Professor.objects.exclude(username_id = user_id)
		employees = Employeeee.objects.exclude(username_id = user_id)

		logged_user = Students.objects.filter(username_id = user_id).first()
		if logged_user is None:
			logged_user = Graduate.objects.filter(username_id = user_id).first()
		if logged_user is None:
			logged_user = Professor.objects.filter(username_id = user_id).first()
		if logged_user is None:
			logged_user = Employeeee.objects.filter(username_id = user_id).first()
		
		followers_objects = StudentFollowing.objects.all()
		#print("followers objects: ", followers_objects)



		if students:
			for i in students:
				#print("students .email :",i.email )
				context1 = {}
				#logged user id
				if followers_objects:
					for j in followers_objects:
						
						if logged_user.email == j.follower_email and i.email == j.following_email:
							
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if graduates:
			for i in graduates:
				context1 = {}
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				#logged user id 
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if professors:
			for i in professors:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
							break
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		if employees:
			for i in employees:
				context1 = {}
				#logged user id 
				if followers_objects:
					for j in followers_objects:
						if logged_user.email == j.follower_email and i.email == j.following_email:
							context1['followText'] = "Unfollow"
						else:
							context1['followText'] = "Follow"
				else:
					context1['followText'] = "Follow"
				context1['user_email'] = logged_user.email
				context1['first_name'] = i.first_name
				context1['surname'] = i.surname
				context1['email'] = i.email
				context1['technical_subject'] = i.technical_subject
				context1['country'] = i.country
				response_list.append(context1)
		#response_list.append(students)
		#response_list.append(graduates)
		#response_list.append(professors)
		#response_list.append(employees)
		#print("all users ",response_list)
		#response_dict.update(response_list)
		#print(response_dict)
		context['all_users'] = response_list
		return context
	def post(self, request):
		try:
			#print('in explore')
			#print('data', request.POST)
			follower_email = request.POST.get('follower_email')
			following_email = request.POST.get('following_email')
			#print('email: ', following_email)
			#print('user id', follower_email)
			#check record if it is exist
			
			status = StudentFollowing.objects.filter(following_email = following_email, follower_email = follower_email).first()
			#status1 = StudentFollowing.objects.filter(following_email = following_email, following_email = following_email).first()
			if status:
				status.delete()
				#print("status ", status)
				return HttpResponse('2')
			else:
				#print("could not found")
				follow_info = StudentFollowing.objects.create( following_email = following_email, follower_email = follower_email)
				follow_info.save()
				return HttpResponse('1')
		except Exception as e:
			#print('error ',e)
			return HttpResponse('3')




###########################Future##########################################
#Graduate dashboard
class FutureDashboard(TemplateView):
	template_name=('mysite/future-dasboard/future-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(FutureDashboard, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list=[]
		comment_list =[]
		user_list = []
		context11 = {}
		obj = Graduate.objects.get(username_id = int(user_id))
		user = User.objects.get(id = user_id)
		context11['user_id'] = obj.id
		context11['user_first_name'] = obj.first_name
		context11['user_sur_name'] = obj.surname
		user_list.append(context11)
		#print("this is logged student :", obj.first_name)
		#print("Graduate obj",obj)
		
		if obj:
			graduate_objects = Graduate.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			students_objects = Students.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			professor_objects = Professor.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			employee_objects = Employeeee.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			follow_users = StudentFollowing.objects.all()
			
			#print("follow users :", follow_users)
			#print("students objects ", student_objects)

			if follow_users:
				for i in follow_users:
					try: 
						student = Students.objects.get(email = i.following_email)
						posts = Existing_student_post.objects.filter(student_user_id = student.username)
						if posts:
							for j in posts:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context1 = {}
								context1['user_id'] = user
								context1['post_id'] = j.id
								context1['user_name'] = j.student_user_id.first_name
								context1['title'] = j.title
								context1['description'] = j.description
								context1['file']= j.file.name
								context1['time_stamp'] = j.time_stamp
								response_list.append(context1)
					except Students.DoesNotExist:
						pass
					
					try:
						graduate = Graduate.objects.get(email = i.following_email)
						posts1 = Future_student_post.objects.filter(future_student_user_id = graduate.username)	
						if posts1:
							for j in posts1:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.future_student_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Graduate.DoesNotExist:
						pass

					try:
						professor = Professor.objects.get(email = i.following_email)

						posts2 = Teacher_post.objects.filter(teacher_user_id = professor.username)	
						if posts2:
							for j in posts2:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.teacher_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Professor.DoesNotExist:
						pass

					try:
						employee = Employeeee.objects.get(email = i.following_email)
						posts3 = Employee_post.objects.filter(employee_user_id = employee.username)	
						if posts3:
							for j in posts3:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.employee_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Employeeee.DoesNotExist:
						pass

			if graduate_objects:
				for i in graduate_objects:
					posts = Future_student_post.objects.filter(future_student_id = i.id)
					#print("posts :", posts)
					
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context1 = {}
							context1['user_id'] = user
							context1['post_id'] = int(j.id)
							context1['user_name'] = j.future_student_user_id.first_name
							context1['title'] = j.title
							context1['description'] = j.description
							context1['file'] = j.file.name
							context1['time_stamp'] =j.time_stamp
							response_list.append(context1)
						#print("response list : graduate ", response_list)
						
			if employee_objects:
				#print("employee objects :",employee_objects)
				for i in employee_objects:
					posts = Employee_post.objects.filter(employee_id = i.id)
					#print("posts :", posts)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context4 = {}
							context4['user_id'] = user
							context4['post_id'] = int(j.id)
							context4['user_name']= j.employee_user_id.first_name
							context4['title']= j.title
							context4['description']= j.description
							context4['file']=j.file.name
							context4['time_stamp']= j.time_stamp
							response_list.append(context4)
						

			if professor_objects:
				for i in professor_objects:
					posts = Teacher_post.objects.filter(teacher_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context3 = {}
							context3['user_id'] = user
							context3['post_id'] = int(j.id)
							context3['user_name'] = j.teacher_user_id.first_name
							context3['title'] = j.title
							context3['description'] = j.description
							context3['file']= j.file.name
							context3['time_stamp'] = j.time_stamp
							response_list.append(context3)

			if students_objects:
				#print("students objects: ", students_objects)
				#print("got students data successfully")
				for i in students_objects:
					#print("student id: ",i.id)
					posts = Existing_student_post.objects.filter(student_id = i.id)
					if posts:
						#print("posts",posts)
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							#print("comments from students posts:1 ", post_comments)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context2={}
							context2['user_name'] = j.student_user_id.first_name
							context2['user_id'] = user
							context2['post_id'] = int(j.id)
							context2['title'] = j.title
							context2['description'] = j.description
							context2['file'] = j.file.name
							context2['time_stamp'] = j.time_stamp
							response_list.append(context2)
						#print("students post have showed")
						#print("got posts from students table")
			
			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			#print('\n\n\n\n\n')
			#print('response_list:',response_list)
		seen = set()
		new_l = []
		for d in response_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				new_l.append(d)

		seen = set()
		comment_new_l = []
		for d in comment_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				comment_new_l.append(d)
		context['all_posts'] = new_l
		context['comments']  = comment_new_l
		context['user'] = user_list
		return context

	def post(self, request):
		#print("this function is for submitting comments.")
		#response_data = {}
		
		comment_text = request.POST.get('comment_text')
		#print("comment text from form", comment_text)
		post_id = request.POST.get('post_id')
		user_id = int(self.request.session['_auth_user_id'])
		
		user = User.objects.filter(id = user_id).first()
		ss_id = Graduate.objects.filter(username_id=int(user_id)).first()
		#print("logged user", user)
		#response_data['comment_text'] = comment
		#response_data['user_id'] = user
		#response_data['post_id'] = post_id
		#print("user :::", user.username)
		if ss_id:
			obj = Comment.objects.create(user_id = user , comment_text = comment_text, post_id = post_id)
			obj.save()
			#return JsonResponse(response_data)
		comments = Comment.objects.all()
		return render(request, 'mysite/future-dasboard/future-dashboard.html',{'comments': comments} )


class FutureProfile(TemplateView):
	template_name=('mysite/future-dasboard/future-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(FutureProfile, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Graduate.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context

class FutureEditProfile(TemplateView):
	template_name=('mysite/future-dasboard/future-edit-profile.html')

class FutureSearchProgram(TemplateView):
	template_name =('mysite/future-dasboard/future-search-program.html')


class FutureAddPost(TemplateView):
	template_name=('mysite/future-dasboard/future-add-post.html')
	
	def get_context_data(self, *args, **kwargs):
		context = super(FutureAddPost, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Future_student_post.objects.filter(future_student_user_id_id=user_id)
		# if obj:
		# 	context['future_post'] = obj
		return context


	def post(self,request):
		
		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		user_id = request.POST.get('user_id')
		file = request.FILES.get('upload_file')
		
		g_id = Graduate.objects.filter(username_id=int(user_id)).first()
		graduate_id = int(g_id.id)
		#print("graduate id: ",graduate_id)
		obj = Future_student_post.objects.create(future_student_id_id = graduate_id,future_student_user_id_id=user_id, title = title, description =description,file= file)
		obj.save()
		#print('future post saved.')
		context={}
		# obj = Future_Student.objects.filter(username_id=user_id)
		# if obj:
		# 	context['future_post'] = obj
		user_id = int(self.request.session['_auth_user_id'])
		response_list=[]
		obj1 = Future_student_post.objects.filter(future_student_user_id_id=user_id)
		
		if obj1:
			for j in obj1:
				context1={}
				context1['user_name'] = j.future_student_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

			response_list.append(context1)
			#print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			#print('\n\n\n\n\n')
			#print('response_list:',response_list)

		context['all_posts'] = response_list

		return redirect('mysite:future-dashboard')
class FutureGroupChat(TemplateView):
	template_name=('mysite/future-dasboard/future-group.html')




###########################Future########################################




###########################Teacher#######################################

class TeacherDashboard(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(TeacherDashboard, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		comment_list = []
		user_list = []
		user = User.objects.get(id = user_id)
		#print(user.username)
		obj = Professor.objects.get(username_id = int(user_id))
		context11  = {}
		context11['user_id'] = obj.id
		context11['user_first_name'] = obj.first_name
		context11['user_sur_name'] = obj.surname
		user_list.append(context11)
		if obj:
			student_objects = Students.objects.filter(country = obj.country, technical_subject=obj.technical_subject)
			graduate_objects = Graduate.objects.filter(country=obj.country, technical_subject=obj.technical_subject)
			professor_objects = Professor.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			employee_objects  = Employeeee.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			follow_users = StudentFollowing.objects.filter(follower_email = user.username)
			
			#print("follow users :", follow_users)
			#print("students objects ", student_objects)

			if follow_users:
				for i in follow_users:
					#print("following user :",i.following_email)
					#print("following user id", i.id)
					try:
						student = Students.objects.get(email = i.following_email)
						#print("student ", student.username)
						posts = Existing_student_post.objects.filter(student_user_id = student.username)
						#print("post of student following :", posts)
						if posts:
							for j in posts:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context1 = {}
								context1['user_id'] = user
								context1['post_id'] = j.id
								context1['user_name'] = j.student_user_id.first_name
								context1['title'] = j.title
								context1['description'] = j.description
								context1['file']= j.file.name
								context1['time_stamp'] = j.time_stamp
								response_list.append(context1)
					except Students.DoesNotExist:
						pass

					
					try:
						graduate = Graduate.objects.get(email = i.following_email)
						posts1 = Future_student_post.objects.filter(future_student_user_id = graduate.username)	
						if posts1:
							for j in posts1:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.future_student_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Graduate.DoesNotExist:
						pass
					

					try:
						professor = Professor.objects.get(email = i.following_email)

						posts2 = Teacher_post.objects.filter(teacher_user_id = professor.username)	
						if posts2:
							for j in posts2:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.teacher_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Professor.DoesNotExist:
						pass

					try:
						employee = Employeeee.objects.get(email = i.following_email)

						posts3 = Employee_post.objects.filter(employee_user_id = employee.username)	
						if posts3:
							for j in posts3:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.employee_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Employeeee.DoesNotExist:
						pass

		if student_objects:
				for i in student_objects:
					#print("this is used to append posts of student objects :", i.email)
					#print("hello : ",i.id)
					posts = Existing_student_post.objects.filter(student_id_id = i.id)
					#print("posts of user :", posts)
					if posts:
						for j in posts:

							#print("post id: within student objects :",j.id)
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							#print("post comments: ", post_comments)
							#print("post id : ",j.id)
							#print("j.student_ user first name :", j.student_user_id.first_name)
							context1 = {}
							context1['user_id'] = user
							#print("student id: ",j.student_id_id)
							context1['post_id'] = int(j.id)
							context1['user_name'] = j.student_user_id.first_name
							context1['title'] = j.title
							context1['description'] = j.description
							context1['file']= j.file.name
							context1['time_stamp'] = j.time_stamp
							response_list.append(context1)
					#print("response list in studnets objects", response_list)	

		if graduate_objects:
				#print("got graduate record")
				for i in graduate_objects:
					posts = Future_student_post.objects.filter(future_student_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							#print("post comments: ", post_comments)
							context4 = {}
							context4['user_id'] = user
							context4['post_id'] = int(j.id)
							context4['user_name']= j.future_student_user_id.first_name
							context4['title'] = j.title
							context4['description'] = j.description
							context4['file']=j.file.name
							context4['time_stamp']=j.time_stamp
							response_list.append(context4)

				#		print("it has posts")
					
		if professor_objects:
				for i in professor_objects:
					posts = Teacher_post.objects.filter(teacher_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							
							context3 = {}
							context3['user_id'] = user
							context3['post_id'] = int(j.id)
							context3['user_name']= j.teacher_user_id.first_name
							context3['title']= j.title
							context3['description'] = j.description
							context3['file'] = j.file.name
							context3['time_stamp'] = j.time_stamp
							response_list.append(context3)
		if employee_objects:
				for i in employee_objects:
					posts = Employee_post.objects.filter(employee_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							
							context2 = {}
							context2['user_id'] = user.username
							context2['post_id'] = int(j.id)
							context2['user_name'] = j.employee_user_id.first_name
							context2['title'] = j.title
							context2['description'] = j.description
							context2['file'] = j.file.name	
							context2['time_stamp'] = j.time_stamp
							response_list.append(context2)		
		
		response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

		#print('\n\n\n\n\n')
		#print('response_list:',response_list)
		seen = set()
		new_l = []
		for d in response_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				new_l.append(d)

		seen = set()
		comment_new_l = []
		for d in comment_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				comment_new_l.append(d)


		context['all_posts'] = new_l
		context['user'] = user_list
		context['comments'] = comment_new_l
		return context
	def post(self, request):
		#print("this function is for submitting comments.")
		#response_data = {}
		
		comment_text = request.POST.get('comment_text')
		#print("comment text from form", comment_text)
		post_id = request.POST.get('post_id')
		user_id = int(self.request.session['_auth_user_id'])
		
		user = User.objects.filter(id = user_id).first()
		ss_id = Professor.objects.filter(username_id=int(user_id)).first()
		#print("logged user", user)
		#response_data['comment_text'] = comment
		#response_data['user_id'] = user
		#response_data['post_id'] = post_id
		#print("user :::", user.username)
		if ss_id:
			obj = Comment.objects.create(user_id = user , comment_text = comment_text, post_id = post_id)
			obj.save()
			#return JsonResponse(response_data)
		comments = Comment.objects.all()
		return render(request, 'mysite/existing-dashboard/existing-dashboard.html',{'comments': comments} )


class TeacherProfile(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(TeacherProfile, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Professor.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context


class TeacherAddPost(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-add-post.html')
	def get_context_data(self, *args, **kwargs):
		context = super(TeacherAddPost, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		# obj = Teacher_post.objects.filter(teacher_user_id_id=user_id)
		# if obj:
		# 	context['teacher_post'] = obj
		return context

	def post(self,request):
		#print('in add employee post')
		#print('data:',request.POST)
		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		file = request.FILES['upload_file']
		user_id = int(self.request.session['_auth_user_id'])
		#print("teacher user id", user_id	)
		ss_id = Professor.objects.filter(username_id=int(user_id)).first()
		#print("Professor",ss_id.id)
		obj = Teacher_post.objects.create(teacher_id_id=int(ss_id.id),teacher_user_id_id=user_id,title=title,description=description,file=file)
		obj.save()
		#print('Professor student post saved.')
		context={}
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Teacher_post.objects.filter(teacher_user_id_id=int(user_id))
		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.teacher_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

				response_list.append(context1)
			#print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			#print('\n\n\n\n\n')
			#print('response_list:',response_list)




		context['all_posts'] = response_list
		return redirect('mysite:teacher-dashboard')

class TeacherEditPost(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-edit-profile.html')


###########################Teacher#######################################



######################ExsitingStudent####################################


class ExistingStudentDashboard(TemplateView):
	template_name = ('mysite/existing-dashboard/existing-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingStudentDashboard, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		#print("user id on dashboard :" , user_id)
		response_list = []
		comment_list = []
		contact_list = []
		user_list = []
		user = User.objects.get(id = user_id)
		#print("user :", user)
		

		posts5 = Existing_student_post.objects.all()
		#print("student posts :",posts5)
		#retrieve logged in student country and technical subject from database
		comments = Comment.objects.all() 
		#print("comments list :", comments)
		obj = Students.objects.get(username_id = int(user_id))
		context11 = {}
		context11['user_id'] = obj.id
		context11['user_first_name'] = obj.first_name
		context11['user_sur_name'] = obj.surname
		user_list.append(context11)
		#print("this is logged student :", obj.first_name)
		if obj:
			student_objects = Students.objects.filter(country = obj.country, technical_subject=obj.technical_subject)
			graduate_objects = Graduate.objects.filter(country=obj.country, technical_subject=obj.technical_subject)
			professor_objects = Professor.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			employee_objects  = Employeeee.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			if student_objects:
				for i in student_objects:
					contact = {}
					contact['id'] = i.id
					contact['first_name'] = i.first_name
					contact['surname'] = i.surname
					contact['email'] = i.email
					contact_list.append(contact)
			#print("contact list", contact_list)

			follow_users = StudentFollowing.objects.all()
			
			#print("follow users :", follow_users)
			#print("students objects ", student_objects)

			if follow_users:
				for i in follow_users:
					try:
						student = Students.objects.get(email = i.following_email)

						posts = Existing_student_post.objects.filter(student_user_id = student.username)
						if posts:
							for j in posts:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context1 = {}
								context1['user_id'] = user
								context1['post_id'] = j.id
								context1['user_name'] = j.student_user_id.first_name
								context1['title'] = j.title
								context1['description'] = j.description
								context1['file']= j.file.name
								context1['time_stamp'] = j.time_stamp
								response_list.append(context1)
					except Students.DoesNotExist:
						pass
					
					try:
						graduate = Graduate.objects.get(email = i.following_email)

						posts1 = Future_student_post.objects.filter(future_student_user_id = graduate.username)	
						if posts1:
							for j in posts1:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.future_student_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Graduate.DoesNotExist:
						pass			
					
					try:
						professor = Professor.objects.get(email = i.following_email)
						posts2 = Teacher_post.objects.filter(teacher_user_id = professor.username)	
						if posts2:
							for j in posts2:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.teacher_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Professor.DoesNotExist:
						pass
					
					try:
						employee = Employeeee.objects.get(email = i.following_email)
						posts3 = Employee_post.objects.filter(employee_user_id = employee.username)	
						if posts3:
							for j in posts3:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.employee_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)		
			
					except Employeeee.DoesNotExist:
						pass
			if student_objects:
				for i in student_objects:
					#print("this is used to append posts of student objects :", i.email)
					#print("hello : ",i.id)
					posts = Existing_student_post.objects.filter(student_id_id = i.id)
					#print("posts of user :", posts)
					if posts:
						for j in posts:

							#print("post id: within student objects :",j.id)
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							#print("post comments: ", post_comments)
							#print("post id : ",j.id)
							#print("j.student_ user first name :", j.student_user_id.first_name)
							context1 = {}
							context1['user_id'] = user
							#print("student id: ",j.student_id_id)
							context1['post_id'] = int(j.id)
							context1['user_name'] = j.student_user_id.first_name
							context1['title'] = j.title
							context1['description'] = j.description
							context1['file']= j.file.name
							context1['time_stamp'] = j.time_stamp
							response_list.append(context1)
					#		print("response list in studnets objects", response_list)
			if graduate_objects:
				#print("got graduate record")
				for i in graduate_objects:
					posts = Future_student_post.objects.filter(future_student_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							#print("post comments: ", post_comments)
							context4 = {}
							context4['user_id'] = user
							context4['post_id'] = int(j.id)
							context4['user_name']= j.future_student_user_id.first_name
							context4['title'] = j.title
							context4['description'] = j.description
							context4['file']=j.file.name
							context4['time_stamp']=j.time_stamp
							response_list.append(context4)

				#		print("it has posts")
					
			if professor_objects:
				for i in professor_objects:
					posts = Teacher_post.objects.filter(teacher_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context3 = {}
							context3['user_id'] = user
							context3['post_id'] = int(j.id)
							context3['user_name']= j.teacher_user_id.first_name
							context3['title']= j.title
							context3['description'] = j.description
							context3['file'] = j.file.name
							context3['time_stamp'] = j.time_stamp
							response_list.append(context3)
			if employee_objects:
				for i in employee_objects:
					posts = Employee_post.objects.filter(employee_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context2 = {}
							context2['user_id'] = user.username
							context2['post_id'] = int(j.id)
							context2['user_name'] = j.employee_user_id.first_name
							context2['title'] = j.title
							context2['description'] = j.description
							context2['file'] = j.file.name	
							context2['time_stamp'] = j.time_stamp
							response_list.append(context2)		
		
			#print(obj.country)
			#print(obj.technical_subject)
			#print("this is student object")
		
	
		response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)
		seen = set()
		new_l = []
		for d in response_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				new_l.append(d)
		seen = set()
		comment_new_l = []
		for d in comment_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				comment_new_l.append(d)

		
		#print("length :",len(response_list))
		#removing duplicate records in list
		
		#print("comment list: ", comment_list)
		#print("length :",len(response_list))
		context['contacts'] = contact_list
		context['all_posts'] = new_l
		context['comments'] = comment_new_l
		context['user'] = user_list
		return context
	def post(self, request):
		#print("this function is for submitting comments.")
		#response_data = {}
		
		comment_text = request.POST.get('comment_text')
		#print("comment text from form", comment_text)
		post_id = request.POST.get('post_id')
		user_id = int(self.request.session['_auth_user_id'])
		
		user = User.objects.filter(id = user_id).first()
		ss_id = Students.objects.filter(username_id=int(user_id)).first()
		#print("logged user", user)
		#response_data['comment_text'] = comment
		#response_data['user_id'] = user
		#response_data['post_id'] = post_id
		#print("user :::", user.username)
		if ss_id:
			obj = Comment.objects.create(user_id = user , comment_text = comment_text, post_id = post_id)
			obj.save()
			#return JsonResponse(response_data)
		comments = Comment.objects.all()
		return render(request, 'mysite/existing-dashboard/existing-dashboard.html',{'comments': comments} )





class ExistingStudentAddPost(TemplateView):
	template_name = ('mysite/existing-dashboard/existing-add-post.html')
	def get_context_data(self,*args,**kwargs):
		context = super(ExistingStudentAddPost, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		return context

	def post(self,request):
		#print('in add employee post')
		#print('data:',request.POST)
		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		file = request.FILES['upload_file']
		user_id = int(self.request.session['_auth_user_id'])
		ss_id = Students.objects.filter(username_id=int(user_id)).first()
		#print("student",ss_id.id)
		obj = Existing_student_post.objects.create(student_id_id=ss_id.id,student_user_id_id=user_id,title=title,description=description,file=file)
		obj.save()
		#print('existing student post saved.')
		context={}
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Existing_student_post.objects.filter(student_user_id_id=int(user_id))
		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.student_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

				response_list.append(context1)
			#print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			#print('\n\n\n\n\n')
			#print('response_list:',response_list)
		context['all_posts'] = response_list
		return redirect('mysite:existing-dashboard')
		#return render(request,'mysite/existing-dashboard/existing-dashboard.html',context)

class ExistingStudentProfile(TemplateView):
	template_name=('mysite/existing-dashboard/existing-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingStudentProfile, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Students.objects.filter(username_id=user_id).first()
		
		if obj:
			#print("this obj has record")
			context['user_info'] = obj
		return context

######################Employeee############################################
	

class EmployeeDashboard(TemplateView):
	template_name=('mysite/employee-dashboard/employee-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(EmployeeDashboard, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		comment_list = []
		user_list = []
		user = User.objects.get(id = user_id)

		obj = Employeeee.objects.get(username_id = int(user_id))
	
		context11 = {}
		context11['user_id'] = obj.id
		context11['user_first_name'] = obj.first_name
		context11['user_sur_name'] = obj.surname
		user_list.append(context11)
		if obj:
			student_objects = Students.objects.filter(country = obj.country, technical_subject=obj.technical_subject)
			graduate_objects = Graduate.objects.filter(country=obj.country, technical_subject=obj.technical_subject)
			professor_objects = Professor.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			employee_objects  = Employeeee.objects.filter(country = obj.country, technical_subject = obj.technical_subject)
			follow_users = StudentFollowing.objects.all()
			
			#print("follow users :", follow_users)
			#print("students objects ", student_objects)

			if follow_users:
				for i in follow_users: # iterate all follow users
					
					try:
						student = Students.objects.get(email = i.following_email ) # fetch following student email from Student Model

						posts = Existing_student_post.objects.filter(student_user_id = student.username) #Fetch all posts from Existing student post model that match with following email
						if posts:
							for j in posts:
								
								post_comments = Comment.objects.filter(post_id = j.id) # fetch all comments related to every post
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context1 = {}
								context1['user_id'] = user
								context1['post_id'] = j.id
								context1['user_name'] = j.student_user_id.first_name
								context1['title'] = j.title
								context1['description'] = j.description
								context1['file']= j.file.name
								context1['time_stamp'] = j.time_stamp
								response_list.append(context1)
					except Students.DoesNotExist:
						pass
					try:
						graduate = Graduate.objects.get(email = i.following_email)
						posts1 = Future_student_post.objects.filter(future_student_user_id = graduate.username)	
						if posts1:
							for j in posts1:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.future_student_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Graduate.DoesNotExist:
						pass

					try:
						professor = Professor.objects.get(email = i.following_email)
						posts2 = Teacher_post.objects.filter(teacher_user_id = professor.username)	
						if posts2:
							for j in posts2:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.teacher_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Professor.DoesNotExist:
						pass
					try:
						employee = Employeeee.objects.get(email = i.following_email)

						posts3 = Employee_post.objects.filter(employee_user_id = employee.username)	
						if posts3:
							for j in posts3:
								post_comments = Comment.objects.filter(post_id = j.id)
								if post_comments:
									for k in post_comments:
										student_comment = Students.objects.filter(email = k.user_id).first()
										graduate_comment = Graduate.objects.filter(email = k.user_id).first()
										professor_comment = Professor.objects.filter(email = k.user_id).first()
										employee_comment = Employeeee.objects.filter(email = k.user_id).first()
										
										#rint("student comment object: ",student_comment.first_name, student_comment.surname)
										#print("graduate comment object: ",graduate_comment)
										#print("professor comment object: ",professor_comment)
										#print("employee comment object: ",employee_comment)
										
										context7 = {}
										if student_comment:
											#print("student comment: ", student_comment)
											context7['commenter_first_name'] = student_comment.first_name 
											context7['commenter_sur_name'] = student_comment.surname 
										elif graduate_comment:
											context7['commenter_first_name'] = graduate_comment.first_name 
											context7['commenter_sur_name'] = graduate_comment.surname 
										elif professor_comment:
											context7['commenter_first_name'] = professor_comment.first_name 
											context7['commenter_sur_name'] = professor_comment.surname 
										elif employee_comment:
											context7['commenter_first_name'] = employee_comment.first_name 
											context7['commenter_sur_name'] = employee_comment.surname 
											
										context7['comment_user_id'] = k.user_id
										context7['comment_text'] = k.comment_text
										context7['post_id'] = int(k.post_id)
										#print("comment user id",i.user_id)
										#print("comment post id", i.post_id)
										#print("comment post text ", i.comment_text)
										comment_list.append(context7)
								context4 = {}
								context4['user_id'] = user
								context4['post_id'] = j.id
								context4['user_name']= j.employee_user_id.first_name
								context4['title'] = j.title
								context4['description'] = j.description
								context4['file']=j.file.name
								context4['time_stamp']=j.time_stamp
								response_list.append(context4)
					except Employeeee.DoesNotExist:
						pass

		if student_objects:
			for i in student_objects:
				#print("this is used to append posts of student objects :", i.email)
				#print("hello : ",i.id)
				posts = Existing_student_post.objects.filter(student_id_id = i.id)
				#print("posts of user :", posts)
				if posts:
					for j in posts:

						#print("post id: within student objects :",j.id)
						post_comments = Comment.objects.filter(post_id = j.id)
						if post_comments:
							for k in post_comments:
								student_comment = Students.objects.filter(email = k.user_id).first()
								graduate_comment = Graduate.objects.filter(email = k.user_id).first()
								professor_comment = Professor.objects.filter(email = k.user_id).first()
								employee_comment = Employeeee.objects.filter(email = k.user_id).first()
								
								#rint("student comment object: ",student_comment.first_name, student_comment.surname)
								#print("graduate comment object: ",graduate_comment)
								#print("professor comment object: ",professor_comment)
								#print("employee comment object: ",employee_comment)
								
								context7 = {}
								if student_comment:
									#print("student comment: ", student_comment)
									context7['commenter_first_name'] = student_comment.first_name 
									context7['commenter_sur_name'] = student_comment.surname 
								elif graduate_comment:
									context7['commenter_first_name'] = graduate_comment.first_name 
									context7['commenter_sur_name'] = graduate_comment.surname 
								elif professor_comment:
									context7['commenter_first_name'] = professor_comment.first_name 
									context7['commenter_sur_name'] = professor_comment.surname 
								elif employee_comment:
									context7['commenter_first_name'] = employee_comment.first_name 
									context7['commenter_sur_name'] = employee_comment.surname 
									
								context7['comment_user_id'] = k.user_id
								context7['comment_text'] = k.comment_text
								context7['post_id'] = int(k.post_id)
								#print("comment user id",i.user_id)
								#print("comment post id", i.post_id)
								#print("comment post text ", i.comment_text)
								comment_list.append(context7)
						#print("post comments: ", post_comments)
						#print("post id : ",j.id)
						#print("j.student_ user first name :", j.student_user_id.first_name)
						context1 = {}
						context1['user_id'] = user
						#print("student id: ",j.student_id_id)
						context1['post_id'] = int(j.id)
						context1['user_name'] = j.student_user_id.first_name
						context1['title'] = j.title
						context1['description'] = j.description
						context1['file']= j.file.name
						context1['time_stamp'] = j.time_stamp
						response_list.append(context1)
				#print("response list in studnets objects", response_list)
			if graduate_objects:
				#print("got graduate record")
				for i in graduate_objects:
					posts = Future_student_post.objects.filter(future_student_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							#print("post comments: ", post_comments)
							context4 = {}
							context4['user_id'] = user
							context4['post_id'] = int(j.id)
							context4['user_name']= j.future_student_user_id.first_name
							context4['title'] = j.title
							context4['description'] = j.description
							context4['file']=j.file.name
							context4['time_stamp']=j.time_stamp
							response_list.append(context4)

				#		print("it has posts")
				
			if professor_objects:
				for i in professor_objects:
					posts = Teacher_post.objects.filter(teacher_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context3 = {}
							context3['user_id'] = user
							context3['post_id'] = int(j.id)
							context3['user_name']= j.teacher_user_id.first_name
							context3['title']= j.title
							context3['description'] = j.description
							context3['file'] = j.file.name
							context3['time_stamp'] = j.time_stamp
							response_list.append(context3)
			if employee_objects:
				for i in employee_objects:
					posts = Employee_post.objects.filter(employee_id_id = i.id)
					if posts:
						for j in posts:
							post_comments = Comment.objects.filter(post_id = j.id)
							if post_comments:
								for k in post_comments:
									student_comment = Students.objects.filter(email = k.user_id).first()
									graduate_comment = Graduate.objects.filter(email = k.user_id).first()
									professor_comment = Professor.objects.filter(email = k.user_id).first()
									employee_comment = Employeeee.objects.filter(email = k.user_id).first()
									
									#rint("student comment object: ",student_comment.first_name, student_comment.surname)
									#print("graduate comment object: ",graduate_comment)
									#print("professor comment object: ",professor_comment)
									#print("employee comment object: ",employee_comment)
									
									context7 = {}
									if student_comment:
										#print("student comment: ", student_comment)
										context7['commenter_first_name'] = student_comment.first_name 
										context7['commenter_sur_name'] = student_comment.surname 
									elif graduate_comment:
										context7['commenter_first_name'] = graduate_comment.first_name 
										context7['commenter_sur_name'] = graduate_comment.surname 
									elif professor_comment:
										context7['commenter_first_name'] = professor_comment.first_name 
										context7['commenter_sur_name'] = professor_comment.surname 
									elif employee_comment:
										context7['commenter_first_name'] = employee_comment.first_name 
										context7['commenter_sur_name'] = employee_comment.surname 
										
									context7['comment_user_id'] = k.user_id
									context7['comment_text'] = k.comment_text
									context7['post_id'] = int(k.post_id)
									#print("comment user id",i.user_id)
									#print("comment post id", i.post_id)
									#print("comment post text ", i.comment_text)
									comment_list.append(context7)
							context2 = {}
							context2['user_id'] = user.username
							context2['post_id'] = int(j.id)
							context2['user_name'] = j.employee_user_id.first_name
							context2['title'] = j.title
							context2['description'] = j.description
							context2['file'] = j.file.name	
							context2['time_stamp'] = j.time_stamp
							response_list.append(context2)		
		

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

		seen = set()
		new_l = []
		for d in response_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				new_l.append(d)

		seen = set()
		comment_new_l = []
		for d in comment_list:
			t = tuple(d.items())
			if t not in seen:
				seen.add(t)
				comment_new_l.append(d)
		context['all_posts'] = new_l
		context['comments'] = comment_new_l
		context['user'] = user_list
		return context
	def post(self, request):
		#print("this function is for submitting comments.")
		#response_data = {}
		
		comment_text = request.POST.get('comment_text')
		#print("comment text from form", comment_text)
		post_id = request.POST.get('post_id')
		user_id = int(self.request.session['_auth_user_id'])
		
		user = User.objects.filter(id = user_id).first()
		ss_id = Employeeee.objects.filter(username_id=int(user_id)).first()
		#print("logged user", user)
		#response_data['comment_text'] = comment
		#response_data['user_id'] = user
		#response_data['post_id'] = post_id
		#print("user :::", user.username)
		if ss_id:
			obj = Comment.objects.create(user_id = user , comment_text = comment_text, post_id = post_id)
			obj.save()
			#return JsonResponse(response_data)
		comments = Comment.objects.all()
		return render(request, 'mysite/employee-dashboard/employee-dashboard.html',{'comments': comments} )

class EmployeeProfile(TemplateView):
	template_name=('mysite/employee-dashboard/employee-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(EmployeeProfile, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Employeeee.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context
#This View is used to add posts in employee dashboard
class EmployeeAddPost(TemplateView):
	template_name=('mysite/employee-dashboard/employee-add-post.html')
	def get_context_data(self,*args,**kwargs):
		context = super(EmployeeAddPost, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		return context

	def post(self,request):
		#print('in add employee post')
		#print('data:',request.POST)
		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		file = request.FILES['upload_file']
		user_id = int(self.request.session['_auth_user_id'])
		#print("user Id: ", user_id)
		ee_id = Employeeee.objects.filter(username_id=int(user_id)).first()
		#print("ee_id :", ee_id)
		employee_id = int(ee_id.id)
		#print("employee id", employee_id)
		obj = Employee_post.objects.create(employee_id_id=employee_id,employee_user_id_id=user_id,title=title,description=description,file=file)
		obj.save()
		#print('employee post saved.')
		context={}
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Employee_post.objects.filter(employee_user_id_id=int(user_id))
		


		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.employee_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

				response_list.append(context1)
			#print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			#print('\n\n\n\n\n')
			#print('response_list:',response_list)




		context['all_posts'] = response_list
		return redirect('mysite:employee-dashboard')

##############Employee#############################################




############ExistingEmployee#######################################

class ExistingEmployeeProfile(TemplateView):
	template_name=('mysite/existing-employee-dashboard/existing-employee-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingEmployeeProfile, self).get_context_data(*args, **kwargs)
		#print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = ExistingEmployee.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context

class ExistingEmployeeDashboard(TemplateView):
	template_name = ('mysite/existing-employee-dashboard/existing-employee-dashboard.html')

class ExistingEmployeeNotification(TemplateView):
	template_name =('mysite/existing-employee-dashboard/existing-employee-notification.html')

class ExistingEmployeeSearchStudent(TemplateView):
	template_name=('mysite/existing-employee-dashboard/existing-employee-search-existing-student.html')

class ExistingEmployeeAddPost(TemplateView):
	template_name =('mysite/existing-employee-dashboard/existing-employee-add-post.html')

 
############ExistingEmployee#######################################


############Registration###########################

#Entrepreneurs is used as Professor Registration
class Entrepreneurs(TemplateView):
	template_name = ('mysite/entrepreneurs-register.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Entrepreneurs, self).get_context_data(*args, **kwargs)
		obj = TechnicalSubject.objects.all()
		#print("This is Technical Subject",obj)
		obj1 = Country.objects.all()
		context['technical_subject'] = obj
		context['country_info'] = obj1
		
		return context



	def post(self,request):
		#print('in Entrepreneurs')
		email = request.POST.get('email')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		country = request.POST.get('country')
		technical_subject = request.POST.get('technical_subject')

		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email, email = email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = False
				user.is_staff = False
				user.save()
				#print("TechnicalSubject:",technical_subject)
				user_info = Professor.objects.create(username_id=user.id,first_name=user.first_name,surname=surname,email=user.username,country_id=country, technical_subject_id = technical_subject)
				user_info.save()
				current_site = get_current_site(request)
				#print("current site",current_site.domain)
				subject = 'Activate your Account'
				message = render_to_string('account_activation_email.txt',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				html_message = render_to_string('activate_account.html',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				user.email_user(subject = subject,message = message, html_message = html_message)

				return HttpResponse('1')

			except Exception as e:
				#print('user error is :',e)
				return HttpResponse('2')
#Employee Registration View class
class Employee(TemplateView):
	template_name = ('mysite/employers-register.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Employee, self).get_context_data(*args, **kwargs)
		obj = TechnicalSubject.objects.all()
		obj2 = Country.objects.all()
		context['technical_subject'] = obj
		context['country_info'] = obj2

		return context

	def post(self,request):
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		email = request.POST.get('email')
		technical_subject = request.POST.get('technical_subject')
		password = request.POST.get('password')
		country = request.POST.get('country')

		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:

			try:
				user = User.objects.create(username=email, email = email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = False
				user.is_staff = False
				user.save()
				user_info = Employeeee.objects.create(username_id=user.id,first_name=user.first_name,email=user.username,surname=surname,technical_subject_id = technical_subject,country_id=country)
				user_info.save()
				current_site = get_current_site(request)
				#print("current site",current_site.domain)
				subject = 'Activate your Account'
				message = render_to_string('account_activation_email.txt',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				html_message = render_to_string('activate_account.html',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				user.email_user(subject = subject,message = message, html_message = html_message)

				return HttpResponse("1")

			except Exception as e:
				#print('user error is :',e)
				return HttpResponse('2')
"""
class ExistingEmployeeRegistration(TemplateView):
	template_name = ('mysite/exisitng-employers-register.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingEmployeeRegistration, self).get_context_data(*args, **kwargs)
		obj = Subjects.objects.all()
		obj1 = Skills.objects.all()
		obj2 = Industry.objects.all()
		obj3 = Country.objects.all()
		obj4 = UserType.objects.all()
		obj5 = Position.objects.all()
		context['subject_info'] = obj
		context['skill_info'] = obj1
		context['industry_info'] = obj2
		context['country_info'] = obj3
		context['user_type_info'] = obj4 
		context['position_info'] = obj5


		return context


	def post(self,request):
		#print('in employee post')
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		date_of_birth = request.POST.get('date_of_birth')
		position_in_company = request.POST.get('position_in_company')
		website_url = request.POST.get('website_url')
		address = request.POST.get('address')
		country = request.POST.get('country')
		email = request.POST.get('email')
		phone_number = request.POST.get('phone_number')
		company_registration_number = request.POST.get('company_registration_number')
		skills = request.POST.get('skills_interested')
		industry = request.POST.get('industry_interested')
		password = request.POST.get('password')


	
		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = False
				
				user.save()
				#print(user.id)
				#print(type(user.id))
				user_info = ExistingEmployee.objects.create(username_id=user.id,first_name=user.first_name,surname=surname,date_of_birth=date_of_birth,email=user.username,position_in_company=position_in_company,website_url=website_url,address=address,country_id=int(country),phone_number=phone_number,company_registration_number=company_registration_number,skills_id=int(skills),industry_id=int(industry))
				user_info.save()
				return HttpResponse('1')

			except Exception as e:
				#print('user errorrr is :',e)
				return HttpResponse('2')

"""
#Graduate Registration Code is in Future_Registration View
class Future_Registration(TemplateView):
	template_name = ('mysite/future_student.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Future_Registration, self).get_context_data(*args, **kwargs)
		obj = TechnicalSubject.objects.all()
		obj1 = StudentType.objects.all()
		obj2 = Country.objects.all()
		context['technical_subject'] = obj
		context['country_info'] = obj2

		return context

	def post(self,request):
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		email = request.POST.get('email')
		technical_subject = request.POST.get('technical_subject')
		password = request.POST.get('password')
		country = request.POST.get('country')

		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email, email = email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = False
				user.is_staff = False
				
				user.save()
				future_student_info = Graduate.objects.create(username_id=user.id,first_name=user.first_name,email=user.username,surname=surname,technical_subject_id = technical_subject,country_id=country)
				future_student_info.save()
				current_site = get_current_site(request)
				#print("current site",current_site.domain)
				subject = 'Activate your Account'
				message = render_to_string('account_activation_email.txt',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				html_message = render_to_string('activate_account.html',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				user.email_user(subject = subject,message = message, html_message = html_message)

				return HttpResponse("1")


			except Exception as e:
				#print('user error is :',e)
				return HttpResponse('2')		
# Student Registration is used for Student Registration
# get_context_data function initialize the registration form with technical subject, student type and location info
class Student_Registration(TemplateView):
	template_name = ('mysite/existing-students.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Student_Registration, self).get_context_data(*args, **kwargs)
		obj = TechnicalSubject.objects.all()
		obj1 = StudentType.objects.all()
		obj2 = Country.objects.all()
		context['technical_subject'] = obj
		context['student_type'] = obj1
		context['country_info'] = obj2
		return context

# this function get the data student dashboard template 
	def post(self,request):
		#print('in post')
		email = request.POST.get('email')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		country = request.POST.get('country')
		technical_subject = request.POST.get('technical_subject')
		student_type = request.POST.get('student_type')
		

		

		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				
				user = User.objects.create(username=email,email = email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = False
				user.is_staff = False
				
				user.save()
				student_info = Students.objects.create(username_id=user.id,first_name=user.first_name,email=user.username,surname=surname,country_id=int(country),technical_subject_id = int(technical_subject), student_type_id = int(student_type))
				student_info.save()
				current_site = get_current_site(request)
				#print("current site",current_site.domain)
				subject = 'Activate your Account'
				message = render_to_string('account_activation_email.txt',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				html_message = render_to_string('activate_account.html',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				user.email_user(subject = subject,message = message, html_message = html_message)

				return HttpResponse('1')

			except Exception as e:
				#print('user error is :',e)
				user = User.objects.filter(username=email)
				#print("user to be delete", user)
				user.delete()
				return HttpResponse('2')

'''
class Teacher_Registration(TemplateView):
	template_name = ('mysite/academics.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Teacher_Registration, self).get_context_data(*args, **kwargs)
		obj = Subjects.objects.all()
		obj1 = Skills.objects.all()
		obj2 = Industry.objects.all()
		obj3 = Country.objects.all()
		obj4 = Title.objects.all()
		obj5 = Position.objects.all()
		context['subject_info'] = obj
		context['skill_info'] = obj1
		context['industry_info'] = obj2
		context['country_info'] = obj3
		context['title_info'] = obj4
		context['position_info'] = obj5

		return context

	def post(self,request):
		#print('in teacher')
		email = request.POST.get('email')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		title = request.POST.get('title')
		university_name = request.POST.get('university_name')
		university_address = request.POST.get('university_address')
		phone_number = request.POST.get('phone_number')
		position = request.POST.get('position')
		programme_title = request.POST.get('programme_title')
		subject_area = request.POST.get('subject_area')

		
		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email, email=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = False
				user.is_staff = False
				
				user.save()

				teacher_info = Teacher.objects.create(username_id=int(user.id),first_name=user.first_name,email=user.username,surname=surname,title_id=int(title),university_name=university_name,university_address=university_address,phone_number=phone_number,position_id=int(position),programme_title=programme_title,subject_area_id=int(subject_area))
				teacher_info.save()
				current_site = get_current_site(request)
				#print("current site",current_site.domain)
				subject = 'Activate your Account'
				message = render_to_string('account_activation_email.txt',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				html_message = render_to_string('activate_account.html',{
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
				user.email_user(subject = subject,message = message, html_message = html_message)

				return HttpResponse("1")

				
			except Exception as e:
				#print('user error is :',e)
				return HttpResponse('2')

'''
######################Other Funtions########################

class Profile(TemplateView):
	template_name=('mysite/profile.html')

class Logout(TemplateView):
	template_name = ('mysite/login.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Logout, self).get_context_data(*args, **kwargs)
		#print('request',self.request)
		if '_auth_user_id' in self.request.session:
			del self.request.session['_auth_user_id'] 
			print('done.')
		return context

# Hold all the registration Prosess for Student, Graduate, Professor, Employee
class Login(TemplateView):
	template_name = ('mysite/login.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Login, self).get_context_data(*args, **kwargs)
		return context 

	def post(self,request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		#print('username:',username)
		#print('password:',password)
		users = User.objects.all()
		#print('all users :', users)
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_superuser == True:
				return HttpResponse('0')
			else:

				obj1 = Students.objects.filter(username_id = int(user.id)).first()
				obj2 = Graduate.objects.filter(username_id = int(user.id)).first()
				obj3 = Professor.objects.filter(username_id = int(user.id)).first()
				obj4 = Employeeee.objects.filter(username_id = int(user.id)).first()
				#print("obj1 student: ", obj1)
				if obj1:
					login(request, user)
					return HttpResponse('1')
				elif obj2: 
					login(request, user)
					return HttpResponse('2')
				elif obj3:
					login(request, user)
					return HttpResponse('3')
				elif obj4:
					login(request, user)
					return HttpResponse('4')
				else:
					return HttpResponse('6')

		else:
			return HttpResponse('7')

######################Other Funtions########################
