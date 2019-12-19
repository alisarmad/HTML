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


class Home(TemplateView):
	template_name=('mysite/index.html')

###########################Future##########################################

class FutureDashboard(TemplateView):
	template_name=('mysite/future-dasboard/future-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(FutureDashboard, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list=[]
		obj1 = Future_student_post.objects.filter(future_student_user_id_id=user_id)
		ids = list(FutureTeacherMapping.objects.filter(future_student_user_id_id=int(user_id)).values_list('connected_teacher_id',flat=True))
		if ids:
			for i in ids:
				obj = Teacher_post.objects.filter(teacher_user_id_id=int(i)).first()
				if obj:
					context1={}
					context1['user_name'] = obj.teacher_user_id.first_name
					context1['title'] = obj.title
					context1['description'] = obj.description
					context1['file'] = obj.file.name
					context1['time_stamp'] = obj.time_stamp
					response_list.append(context1)

		if obj1:
			for j in obj1:
				context1={}
				context1['user_name'] = j.future_student_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

			response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)

		context['all_posts'] = response_list
		return context

class FutureProfile(TemplateView):
	template_name=('mysite/future-dasboard/future-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(FutureProfile, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Future_Student.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context

class FutureEditProfile(TemplateView):
	template_name=('mysite/future-dasboard/future-edit-profile.html')

class FutureSearchProgram(TemplateView):
	template_name =('mysite/future-dasboard/future-search-program.html')

class Future_Search_Result(TemplateView):
	template_name =('mysite/future-dasboard/future-search-program.html')
	def post(self,request):
		print('in post result ')
		print('data:',request.POST)
		search = request.POST.get('search')
		logged_id = request.POST.get('logged_id')
		remove_list =[]
		response_list =[]
		remove2 =[]
		all_ids = list(Teacher.objects.filter(programme_title__icontains=str(search)).values_list('username_id',flat=True))
		if all_ids:
			print('all_ids',all_ids)
			connected_teacher_ids = list(FutureTeacherMapping.objects.filter(future_student_user_id=int(logged_id)).values_list('connected_teacher_id',flat=True))
			if connected_teacher_ids:
				for i in all_ids:
					if i in connected_teachers:
						remove_list.append(i)

				for k in remove:
					all_ids.remove(k)

			final_ids = all_ids
			print('final_ids after connectin filter',final_ids)

			pending_notification_ids = list(TeacherFutureNotifications.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_id_id',flat=True))

			if pending_notification_ids:
				print('notification_ids',pending_notification_ids)
				for i in final_ids:
					if i in pending_notification_ids:
						remove2.append(i)

				for k in remove2:
					final_ids.remove(k)

				print('final_ids after pending filter',final_ids)

			print('final',final_ids)

			if final_ids:
				for i in final_ids:
					obj = Teacher.objects.filter(username_id=int(i)).first()
					if obj:
						context = {}
						context['first_name'] = obj.first_name
						context['surname'] = obj.surname
						context['programme_title'] = obj.programme_title
						context['username_id'] = obj.username.id
						context['logged_id'] = logged_id

						response_list.append(context)		
				return HttpResponse(json.dumps(response_list))
			else:
				return HttpResponse('0')
		else:
			return HttpResponse('0')
			
class FutureTeacherFollowing(TemplateView):
	template_name=('mysite/future-dasboard/future-teacher-following.html')
	def get_context_data(self, *args, **kwargs):
		context = super(FutureTeacherFollowing, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		ids = list(FutureTeacherMapping.objects.filter(future_student_user_id_id=int(user_id)).values_list('connected_teacher_id',flat=True))
		if ids:
			for i in ids:
				obj = Teacher.objects.filter(username_id=int(i)).first()
				if obj:
					context1={}
					context1['name'] = obj.first_name
					context1['programme_title'] = obj.programme_title
					context1['username'] = obj.username.id
					response_list.append(context1)

			context['already_added'] = response_list

		return context

class FutureAddPost(TemplateView):
	template_name=('mysite/future-dasboard/future-add-post.html')

	def get_context_data(self, *args, **kwargs):
		context = super(FutureAddPost, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Future_student_post.objects.filter(future_student_user_id_id=user_id)
		# if obj:
		# 	context['future_post'] = obj
		return context


	def post(self,request):
		print('in future post')
		print('data:',request.POST)
		print('file data:',request.FILES)

		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		user_id = request.POST.get('user_id')
		file = request.FILES.get('upload_file')
		obj = Future_Student.objects.filter(username_id=int(user_id)).first()
		future_student_id = int(obj.id)
		future_student_user_id = int(user_id)
		obj1 = Future_student_post.objects.create(title=title,description=description,file=file,future_student_id_id=future_student_id,future_student_user_id_id=future_student_user_id)
		obj1.save()
		print('future post saved.')
		context={}
		# obj = Future_Student.objects.filter(username_id=user_id)
		# if obj:
		# 	context['future_post'] = obj
		user_id = int(self.request.session['_auth_user_id'])
		response_list=[]
		obj1 = Future_student_post.objects.filter(future_student_user_id_id=user_id)
		ids = list(FutureTeacherMapping.objects.filter(future_student_user_id_id=int(user_id)).values_list('connected_teacher_id',flat=True))
		if ids:
			for i in ids:
				obj = Teacher.objects.filter(username_id=int(i)).first()
				if obj:
					context1={}
					context1['user_name'] = k.teacher_user_id.first_name
					context1['title'] = k.title
					context1['description'] = k.description
					context1['file'] = k.file.name
					context1['time_stamp'] = k.time_stamp
					response_list.append(context1)

		if obj1:
			for j in obj1:
				context1={}
				context1['user_name'] = j.future_student_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

			response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)

		context['all_posts'] = response_list

		return render(request,'mysite/future-dasboard/future-dashboard.html',context)

class FutureNotification(TemplateView):
	template_name=('mysite/future-dasboard/future-notification.html')
	def get_context_data(self, *args, **kwargs):
		context = super(FutureNotification, self).get_context_data(*args, **kwargs)
		check_id = self.request.session['_auth_user_id']
		print(check_id)
		response_list =[]
		obj = TeacherFutureNotifications.objects.filter(sending_id_id=int(check_id),pending=True)
		print('hellll')
		print(obj)
		if obj:
			for i in obj:
				context1={}
				context1['first_name'] = i.logged_id.first_name
				context1['id'] = i.id
				response_list.append(context1)
			context['notification'] = response_list

		print(context)

		return context

def future_teacher_create_notification(request,id1,id2):
	if request.method == 'GET':
		print('logged_id',id1)
		print('username_id',id2)
		obj = TeacherFutureNotifications.objects.create(logged_id_id=int(id1),sending_id_id=int(id2))
		obj.save()
		print('noti saved done.')
		return HttpResponse('0')
	else:
		return HttpResponse('1')

def future_teacher_accept_notification(request,id1,id2):
	if request.method == 'GET':
		print('notification_id',id1)
		print('logged_id',id2)
		notification_id = id1
		logged_id = id2
		obj = Future_Student.objects.filter(username_id=int(logged_id)).first()
		if obj:
			student_id = int(obj.id)
			print('accepter is future student.')
			obj1 = TeacherFutureNotifications.objects.filter(id=int(notification_id)).first()
			if obj1:
				obj1.pending = False
				obj1.save()
				print('pending status changed.')
				future_user_id = int(obj1.sending_id_id)
				connected_teacher_user_id = int(obj1.logged_id_id)
				print('future_student_id',future_user_id)
				print('to_be_connected_teacher',connected_teacher_user_id)
				print('obj for FutureTeacherMapping')
				obj2 = FutureTeacherMapping.objects.filter(future_student_user_id_id=int(future_user_id),connected_teacher_id_id=int(connected_teacher_user_id)).first()
				if obj2:
					print('already connected.1')
				else:
					obj3 = FutureTeacherMapping.objects.create(future_student_user_id_id=int(future_user_id),connected_teacher_id_id=int(connected_teacher_user_id))
					obj3.save()
					print('connection form future side added side added.1')


				print('\n\n\n\n')
				teacher_user_id = int(obj1.logged_id_id)
				tt_id = Teacher.objects.filter(username_id=int(teacher_user_id)).first()
				teacher_id = int(tt_id.id)
				connected_future_user_id = int(obj1.sending_id_id)
				print('teacher_user_id',teacher_user_id)
				print('connected_future_user_id',connected_future_user_id)
				print('obj for TeacherFutureMapping')
				obj4 = TeacherFutureMapping.objects.filter(teacher_user_id_id=int(teacher_user_id),connected_future_student_id_id=int(connected_future_user_id)).first()
				if obj4:
					print('already connected.2')
				else:
					obj5 = TeacherFutureMapping.objects.create(teacher_user_id_id=int(teacher_user_id),connected_future_student_id_id=int(connected_future_user_id))
					obj5.save()
					print('connection from teacher side added.1')

				return HttpResponse('0')


		ob2 = Teacher.objects.filter(username_id=int(logged_id)).first()
		if ob2:
			teacher_id = int(ob2.id)
			print('accepter is teacher.')
			obj1 = TeacherFutureNotifications.objects.filter(id=int(notification_id)).first()
			if obj1:
				obj1.pending = False
				obj1.save()
				print('pending status changed.')
				teacher_user_id = int(obj1.sending_id_id)
				connected_future_user_id = int(obj1.logged_id_id)
				print('teacher_user_id',teacher_user_id)
				print('connected_future_user_id',connected_future_user_id)
				print('obj for TeacherFutureMapping')
				obj2 = TeacherFutureMapping.objects.filter(teacher_user_id_id=int(teacher_user_id),connected_future_student_id_id=int(connected_future_user_id)).first()
				if obj2:
					print('already connected 1.')
				else:
					obj3 = TeacherFutureMapping.objects.create(teacher_user_id_id=int(teacher_user_id),connected_future_student_id_id=int(connected_future_user_id))
					obj3.save()
					print('connection from teacher side added.2')


				print('\n\n\n\n\n')
				future_user_id = int(obj1.logged_id_id)
				s_id = Future_Student.objects.filter(username_id=int(future_user_id)).first()
				future_student_id = int(s_id.id)
				connected_teacher_user_id = int(obj1.sending_id_id)
				print('future_student_id',future_student_id)
				print('connected_teacher_user_id',connected_teacher_user_id)
				print('obj for FutureTeacherMapping')
				obj4 = FutureTeacherMapping.objects.filter(future_student_user_id_id=int(future_user_id),connected_teacher_id_id=int(connected_teacher_user_id),future_id_id=int(future_student_id)).first()
				if obj4:
					print('already connected 2.')
				else:
					obj5 = FutureTeacherMapping.objects.create(future_student_user_id_id=int(future_user_id),connected_teacher_id_id=int(connected_teacher_user_id),future_id_id=int(future_student_id))
					obj5.save()
					print('connection form future side added.2')

				return HttpResponse('0')


		print('in accept notification')
		return HttpResponse('0')
	else:
		return HttpResponse('1')

def future_teacher_delete_notification(request,id1):
	if request.method == 'GET':
		print('notification_id',id1)
		obj = TeacherFutureNotifications.objects.filter(id=int(id1)).first()
		if obj:
			obj.delete()
			print('noti deleted.')
		return HttpResponse('0')
	else:
		return HttpResponse('1')

def future_teacher_unfollow(request,id1,id2):
	if request.method == 'GET':
		print('logged_id',id1)
		print('unlogged_id',id2)
		logged_id = id1
		unlogged_id = id2
		obj = Future_Student.objects.filter(username_id=int(logged_id)).first()
		if obj:
			future_id = int(obj.id)
			print('doer is future student.')
			future_user_id = int(logged_id)
			connected_teacher_user_id = int(unlogged_id)
			print('future_user_id',future_user_id)
			print('connected_teacher_user_id',connected_teacher_user_id)
			print('obj for StudentEmployeeMapping')
			obj2 = FutureTeacherMapping.objects.filter(future_student_user_id_id=int(future_user_id),connected_teacher_id_id=int(connected_teacher_user_id)).first()
			if obj2:
				print('exist to unfollow')
				obj2.delete()
				print('connection deleted when doer is future student.1')
			else:
				print('no connection is there to unfollow between teacher and future student.1')

			print('done 1.')


			print('\n\n\n\n\n')
			teacher_user_id = int(unlogged_id)
			s_id = Teacher.objects.filter(username_id=int(unlogged_id)).first()
			teacher_id = int(s_id.id)
			connected_future_user_id = int(logged_id)
			print('teacher_user_id',teacher_user_id)
			print('connected_future_user_id',connected_future_user_id)
			print('obj for TeacherFutureMapping')
			obj4 = TeacherFutureMapping.objects.filter(teacher_user_id_id=int(teacher_user_id),connected_future_student_id_id=int(connected_future_user_id)).first()
			if obj4:
				print('exist to unfollow')
				obj4.delete()
				print('connection deleted from employee side when the doer existing student.2')
				return HttpResponse('0')
			else:
				print('no connection is there to unfollow between employee and exsiting student.2')

			return HttpResponse('0')


		ob2 = Teacher.objects.filter(username_id=int(logged_id)).first()
		if ob2:
			teacher_id = int(ob2.id)
			print('doer is teacher.')
			teacher_user_id = int(logged_id)
			connected_employee_user_id = int(unlogged_id)
			print('teacher_user_id',teacher_user_id)
			print('connected_employee_user_id',connected_employee_user_id)
			print('obj for EmployeeStudentMapping')
			obj3 = TeacherFutureMapping.objects.filter(teacher_user_id_id=int(teacher_user_id),connected_future_student_id_id=int(connected_employee_user_id)).first()
			if obj3:
				print('exist to unfollow')
				obj3.delete()
				print('connection deleted when doer is teacher.3')
			else:
				print('no connection is there to unfollow between teacher and future student.3')

			print('done 2.')

			print('\n\n\n\n\n')
			future_user_id = int(unlogged_id)
			f_id = Future_Student.objects.filter(username_id=int(unlogged_id)).first()
			future_id = int(f_id.id)
			connected_teacher_user_id = int(logged_id)
			print('future_user_id',future_user_id)
			print('connected_teacher_user_id',connected_teacher_user_id)
			print('obj for FutureTeacherMapping')
			obj4 = FutureTeacherMapping.objects.filter(future_student_user_id_id=int(future_user_id),connected_teacher_id=int(connected_teacher_user_id)).first()
			if obj4:
				print('exist to unfollow')
				obj4.delete()
				print('connection deleted when doer is teacher.4')
				return HttpResponse('0')
			else:
				print('no connection is there to unfollow between teacher and future student.3')

			return HttpResponse('0')


		else:
			return HttpResponse('0')
	else:
		return HttpResponse('0')

class FutureGroupChat(TemplateView):
	template_name=('mysite/future-dasboard/future-group.html')




###########################Future########################################




###########################Teacher#######################################

class TeacherDashboard(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(TeacherDashboard, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Teacher_post.objects.filter(teacher_user_id_id=user_id)
		ids = list(TeacherFutureMapping.objects.filter(teacher_user_id_id=int(user_id)).values_list('connected_future_student_id_id',flat=True))
		if ids:
			print('ids',ids)
			for i in ids:
				obj2 = Future_student_post.objects.filter(future_student_user_id_id=int(i))
				for k in obj2:
					context1 ={}
					context1['user_name'] = k.future_student_user_id.first_name
					context1['title'] = k.title
					context1['description'] = k.description
					context1['file'] = k.file.name
					context1['time_stamp'] = k.time_stamp
					response_list.append(context1)


		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.teacher_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

			response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)




		context['all_posts'] = response_list
		return context

class TeacherProfile(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(TeacherProfile, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Teacher.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context

class TeacherSearchFuture(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-search-future-student.html')
	def get_context_data(self, *args, **kwargs):
		context = super(TeacherSearchFuture, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list =[]
		ids = (TeacherFutureMapping.objects.filter(teacher_user_id_id=int(user_id)).values_list('connected_future_student_id_id',flat=True))
		if ids:
			for i in ids:
				obj = Future_Student.objects.filter(username_id=int(i))
				if obj:
					for k in obj:
						context1={}
						context1['first_name'] = k.first_name
						context1['subject_interested'] = k.subject_interested
						context1['username'] = k.username.id
						response_list.append(context1)

			context['already_added'] = response_list
			print('context',context)

		return context

	def post(self,request):
		print('in post result ')
		print('data:',request.POST)
		search = request.POST.get('search')
		logged_id = request.POST.get('logged_id')
		remove1 =[]
		remove2 =[]
		response_list=[]

		# obj = Teacher.objects.filter(programme_title__icontains=str(search))
		all_ids = list(Future_Student.objects.filter(subject_interested__name__icontains=str(search)).values_list('username_id',flat=True))
		print('all_ids',all_ids)
		if all_ids:
			connected_future_ids = list(TeacherFutureMapping.objects.filter(teacher_user_id_id=int(logged_id)).values_list('connected_future_student_id_id',flat=True))
			if connected_future_ids:
				print('connected_future_ids',connected_future_ids)
				for i in all_ids:
					if i in connected_future_ids:
						remove1.append(i)

					if remove1:
						for k in remove1:
							if k in all_ids:
								all_ids.remove(k)

				print('ids after connection filter',all_ids)

			final_ids = all_ids

			pending_notification_ids = list(TeacherFutureNotifications.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_id_id',flat=True))
			if pending_notification_ids:
				print('pending notification ids',pending_notification_ids)
				for i in final_ids:
					if i in pending_notification_ids:
						remove2.append(i)

					if remove2:
						for i in remove2:
							if i in final_ids:
								final_ids.remove(i)


				print('after pending filter',final_ids)

			response_list = []

			if final_ids:
				for i in final_ids:
					obj = Future_Student.objects.filter(username_id=int(i)).first()
					if obj:
						context = {}
						context['first_name'] = obj.first_name
						context['surname'] = obj.surname
						context['subject_interested'] = obj.subject_interested.name
						context['username_id'] = obj.username.id
						context['logged_id'] = logged_id

						response_list.append(context)		
				return HttpResponse(json.dumps(response_list))
			else:
				return HttpResponse('0')
		else:
			return HttpResponse('0')	

class TeacherSearchExist(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-search-existing-student.html')

class TeacherAddPost(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-add-post.html')
	def get_context_data(self, *args, **kwargs):
		context = super(TeacherAddPost, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		# obj = Teacher_post.objects.filter(teacher_user_id_id=user_id)
		# if obj:
		# 	context['teacher_post'] = obj
		return context

	def post(self,request):
		print('in teacher post')
		print('data:',request.POST)
		print('file data:',request.FILES)

		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		user_id = request.POST.get('user_id')
		file = request.FILES.get('upload_file')
		obj = Teacher.objects.filter(username_id=int(user_id)).first()
		teacher_id = int(obj.id)
		teacher_user_id = int(user_id)
		obj1 = Teacher_post.objects.create(title=title,description=description,file=file,teacher_id_id=teacher_id,teacher_user_id_id=teacher_user_id)
		obj1.save()
		print('teacher post saved.')
		context={}
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Teacher_post.objects.filter(teacher_user_id_id=user_id)
		ids = list(TeacherFutureMapping.objects.filter(teacher_user_id_id=int(user_id)).values_list('connected_future_student_id',flat=True))
		if ids:
			for i in ids:
				obj2 = Future_student_post.objects.filter(future_student_user_id_id=int(i))
				for k in obj2:
					context1 ={}
					context1['user_name'] = k.future_student_user_id.first_name
					context1['title'] = k.title
					context1['description'] = k.description
					context1['file'] = k.file.name
					context1['time_stamp'] = k.time_stamp

				response_list.append(context1)


		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.teacher_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

			response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)




		context['all_posts'] = response_list
		return render(request,'mysite/teacher-dashboard/teacher-dashboard.html',context)

class TeacherEditPost(TemplateView):
	template_name=('mysite/teacher-dashboard/teacher-edit-profile.html')

class TeacherNotification(TemplateView):
	template_name = ('mysite/teacher-dashboard/teacher-notification.html')
	def get_context_data(self, *args, **kwargs):
		print('in teacher notification.')
		context = super(TeacherNotification, self).get_context_data(*args, **kwargs)
		check_id = self.request.session['_auth_user_id']
		response_list=[]
		print(check_id)
		obj = TeacherFutureNotifications.objects.filter(sending_id_id=int(check_id),pending=True)	
		if obj:
			print(obj)	
			for i in obj:
				context1={}
				context1['notification_id'] = i.id
				context1['logged_id'] = i.logged_id.id
				context1['sending_id'] = i.sending_id.id
				context1['first_name'] = i.logged_id.first_name
				context1['id'] = i.id
				response_list.append(context1)

		obj1 = TeacherStudentNotification.objects.filter(sending_ids_id=int(check_id),pending=True)
		if obj1:
			print(obj1)
			for i in obj1:
				context1={}
				context1['notification_id'] = i.id
				context1['logged_id'] = i.logged_id.id
				context1['sending_id'] = i.sending_id.id
				context1['first_name'] = i.logged_id.first_name
				context1['id'] = i.id
				response_list.append(context1)



			# response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)
		context['notification'] = response_list
		print(context)
		return context


###########################Teacher#######################################



######################ExsitingStudent####################################


class ExistingStudentDashboard(TemplateView):
	template_name = ('mysite/existing-dashboard/existing-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingStudentDashboard, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Existing_student_post.objects.filter(student_user_id_id=int(user_id))
		obj1 = StudentEmployeeMapping.objects.filter(student_user_id_id=int(user_id)).values_list('connected_employee_user_id_id',flat=True)
		if obj1:
			for i in obj1:
				objj = Employee_post.objects.filter(employee_user_id_id=int(i))
				if objj:
					for k in objj:
						context1 ={}
						context1['user_name'] = k.employee_user_id.first_name
						context1['title'] = k.title
						context1['description'] = k.description
						context1['file'] = k.file.name
						context1['time_stamp'] = k.time_stamp

						response_list.append(context1)


		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.student_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

				response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)




		context['all_posts'] = response_list
		return context

class ExistingStudentAddPost(TemplateView):
	template_name = ('mysite/existing-dashboard/existing-add-post.html')
	def get_context_data(self,*args,**kwargs):
		context = super(ExistingStudentAddPost, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		return context

	def post(self,request):
		print('in add employee post')
		print('data:',request.POST)
		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		file = request.FILES['upload_file']
		user_id = int(self.request.session['_auth_user_id'])
		ss_id = Students.objects.filter(username_id=int(user_id)).first()
		student_id = int(ss_id.id)
		obj = Existing_student_post.objects.create(student_user_id_id=int(user_id),student_id_id=int(student_id),title=title,description=description,file=file)
		obj.save()
		print('existing student post saved.')
		context={}
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Existing_student_post.objects.filter(student_user_id_id=int(user_id))
		obj1 = StudentEmployeeMapping.objects.filter(student_user_id_id=int(user_id)).values_list('connected_employee_user_id_id',flat=True)
		if obj1:
			for i in obj1:
				objj = Employee_post.objects.filter(employee_user_id_id=int(i))
				if objj:
					for k in objj:
						context1 ={}
						context1['user_name'] = k.employee_user_id.first_name
						context1['title'] = k.title
						context1['description'] = k.description
						context1['file'] = k.file.name
						context1['time_stamp'] = k.time_stamp

						response_list.append(context1)


		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.student_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

				response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)




		context['all_posts'] = response_list
		return render(request,'mysite/existing-dashboard/existing-dashboard.html',context)

class ExistingStudentProfile(TemplateView):
	template_name=('mysite/existing-dashboard/existing-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingStudentProfile, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = Students.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context

class ExistingStudentNotification(TemplateView):
	template_name=('mysite/existing-dashboard/existing-notification.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingStudentNotification, self).get_context_data(*args, **kwargs)
		check_id = self.request.session['_auth_user_id']
		print(check_id)
		obj = StudentEmployeeNotification.objects.filter(sending_ids_id=int(check_id),pending=True)
		print('hellll')
		print(obj)
		if obj:
			context['notification'] = obj

		print('context:',context)

		return context

class ExistingStudentSearch(TemplateView):
	template_name=('mysite/existing-dashboard/existing-search-existing-student.html')
	def get_context_data(self,*args,**kwargs):
		context = super(ExistingStudentSearch, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		return context

	def post(self,request):
		print('in post result ')
		print('data:',request.POST)
		search = request.POST.get('search')
		logged_id = request.POST.get('logged_id')
		remove = []
		response_list = []
		skills_ids = list(User_Info.objects.filter(skills__name__icontains=str(search),user_type_id=2).values_list('username_id',flat=True))
		industry_ids = list(User_Info.objects.filter(industry__name__icontains=str(search),user_type_id=2).values_list('username_id',flat=True))

		if skills_ids and industry_ids:
			print('both found.')
			skills_ids = set(skills_ids)
			industry_ids = set(industry_ids)
			combine_ids = skills_ids | industry_ids
			final_ids = list(combine_ids)
			connected_ids = list(StudentEmployeeMapping.objects.filter(student_user_id_id=int(logged_id)).values_list('connected_employee_user_id_id',flat=True))
			print('connected_ids',connected_ids)
			print('final_ids',final_ids)
			if connected_ids:
				for i in final_ids:
					if i in connected_ids:
						remove.append(i)
				if remove :
					for k in remove:
						final_ids.remove(k)
			print('after final_ids',final_ids)


			if final_ids:
				remove1=[]
				pending_notification_ids = list(StudentEmployeeNotification.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_ids_id',flat=True))
				if pending_notification_ids:
					print('pending_ids:',pending_notification_ids)
					for i in final_ids:
						if i in pending_notification_ids:
							remove1.append(i)

					if remove1:
						for k in remove1:
							final_ids.remove(k)
			if final_ids:
				for i in final_ids:
					obj = User_Info.objects.filter(username_id=int(i)).first()
					if obj:
						context = {}
						context['first_name'] = obj.first_name
						context['surname'] = obj.surname
						context['skills'] = obj.skills.name
						context['industry'] = obj.industry.name
						context['username_id'] = obj.username.id
						context['logged_id'] = logged_id

						response_list.append(context)	

				return HttpResponse(json.dumps(response_list))
			else:
				return HttpResponse('0')
			
		else:
			if skills_ids:
				print('only skills match found.')
				final_ids = skills_ids
				connected_ids = list(StudentEmployeeMapping.objects.filter(student_user_id_id=int(logged_id)).values_list('connected_employee_user_id_id',flat=True))
				print('connected_ids',connected_ids)
				print('final_ids',final_ids)
				if connected_ids:
					for i in final_ids:
						if i in connected_ids:
							remove.append(i)
					if remove :
						for k in remove:
							final_ids.remove(k)
				print('after final_ids',final_ids)

				if final_ids:
					remove1=[]
					pending_notification_ids = list(StudentEmployeeNotification.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_ids_id',flat=True))
					if pending_notification_ids:
						print('pending_ids:',pending_notification_ids)
						for i in final_ids:
							if i in pending_notification_ids:
								remove1.append(i)

						if remove1:
							for k in remove1:
								final_ids.remove(k)
				if final_ids:
					for i in final_ids:
						obj = User_Info.objects.filter(username_id=int(i)).first()
						if obj:
							context = {}
							context['first_name'] = obj.first_name
							context['surname'] = obj.surname
							context['skills'] = obj.skills.name
							context['industry'] = obj.industry.name
							context['username_id'] = obj.username.id
							context['logged_id'] = logged_id

							response_list.append(context)	

					return HttpResponse(json.dumps(response_list))
				else:
					return HttpResponse('0')

			elif industry_ids:
				print('only industry match found.')
				final_ids = industry_ids
				connected_ids = list(StudentEmployeeMapping.objects.filter(student_user_id_id=int(logged_id)).values_list('connected_employee_user_id_id',flat=True))
				print('connected_ids',connected_ids)
				print('final_ids',final_ids)
				if connected_ids:
					for i in final_ids:
						if i in connected_ids:
							remove.append(i)
					if remove :
						for k in remove:
							final_ids.remove(k)
				

				if final_ids:
					remove1=[]
					pending_notification_ids = list(StudentEmployeeNotification.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_ids_id',flat=True))
					if pending_notification_ids:
						print('pending_ids:',pending_notification_ids)
						for i in final_ids:
							if i in pending_notification_ids:
								remove1.append(i)

						if remove1:
							for k in remove1:
								final_ids.remove(k)

				print('after final_ids',final_ids)


				if final_ids:
					for i in final_ids:
						obj = User_Info.objects.filter(username_id=int(i)).first()
						if obj:
							context = {}
							context['first_name'] = obj.first_name
							context['surname'] = obj.surname
							context['skills'] = obj.skills.name
							context['industry'] = obj.industry.name
							context['username_id'] = obj.username.id
							context['logged_id'] = logged_id

							response_list.append(context)

					return HttpResponse(json.dumps(response_list))
				else:
					return HttpResponse('0')
			else:
				print('not found.')
				return HttpResponse('0')

class ExistingStudentFollowingEmployees(TemplateView):
	template_name =('mysite/existing-dashboard/existing-followers-employee.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingStudentFollowingEmployees, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = StudentEmployeeMapping.objects.filter(student_user_id_id=user_id).values_list('connected_employee_user_id_id',flat=True)
		if obj:
			print(obj)
			for i in obj:
				obj1 = User_Info.objects.filter(username_id=int(i)).first()
				if obj1:
					context1={}
					context1['first_name'] = obj1.first_name
					context1['skills'] = obj1.skills.name
					context1['industry'] = obj1.industry.name
					context1['username_id'] = obj1.username.id
					response_list.append(context1)

			context['already_added'] = response_list
			print(context)

		return context


######################ExsitingStudent######################################


######################Employeee############################################
	

class EmployeeDashboard(TemplateView):
	template_name=('mysite/employee-dashboard/employee-dashboard.html')
	def get_context_data(self, *args, **kwargs):
		context = super(EmployeeDashboard, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Employee_post.objects.filter(employee_user_id_id=int(user_id))
		obj1 = EmployeeStudentMapping.objects.filter(employee_user_id_id=int(user_id)).values_list('connected_student_user_id_id',flat=True)
		if obj1:
			for i in obj1:
				objj = Existing_student_post.objects.filter(student_user_id_id=int(i))
				if objj:
					for k in objj:
						context1 ={}
						context1['user_name'] = k.student_user_id.first_name
						context1['title'] = k.title
						context1['description'] = k.description
						context1['file'] = k.file.name
						context1['time_stamp'] = k.time_stamp

						response_list.append(context1)


		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.employee_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

				response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)




		context['all_posts'] = response_list
		return context

class EmployeeProfile(TemplateView):
	template_name=('mysite/employee-dashboard/employee-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(EmployeeProfile, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		obj = User_Info.objects.filter(username_id=user_id).first()
		if obj:
			context['user_info'] = obj
		return context

class EmployeeAddPost(TemplateView):
	template_name=('mysite/employee-dashboard/employee-add-post.html')
	def get_context_data(self,*args,**kwargs):
		context = super(EmployeeAddPost, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		return context

	def post(self,request):
		print('in add employee post')
		print('data:',request.POST)
		title = request.POST.get('post_title')
		description = request.POST.get('post_text')
		file = request.FILES['upload_file']
		user_id = int(self.request.session['_auth_user_id'])
		ee_id = User_Info.objects.filter(username_id=int(user_id)).first()
		employee_id = int(ee_id.id)
		obj = Employee_post.objects.create(employee_user_id_id=int(user_id),employee_id_id=int(employee_id),title=title,description=description,file=file)
		obj.save()
		print('employee post saved.')
		context={}
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = Employee_post.objects.filter(employee_user_id_id=int(user_id))
		obj1 = EmployeeStudentMapping.objects.filter(employee_user_id_id=int(user_id)).values_list('connected_student_user_id_id',flat=True)
		if obj1:
			for i in obj1:
				objj = Existing_student_post.objects.filter(student_user_id_id=int(i))
				if objj:
					for k in objj:
						context1 ={}
						context1['user_name'] = k.student_user_id.first_name
						context1['title'] = k.title
						context1['description'] = k.description
						context1['file'] = k.file.name
						context1['time_stamp'] = k.time_stamp

						response_list.append(context1)


		if obj:
			for j in obj:
				context1 ={}
				context1['user_name'] = j.employee_user_id.first_name
				context1['title'] = j.title
				context1['description'] = j.description
				context1['file'] = j.file.name
				context1['time_stamp'] = j.time_stamp

				response_list.append(context1)
			print('before:',response_list)

			response_list = sorted(response_list, key=lambda k: k['time_stamp'], reverse=True)

			print('\n\n\n\n\n')
			print('response_list:',response_list)




		context['all_posts'] = response_list
		return render(request,'mysite/employee-dashboard/employee-dashboard.html',context)

class EmployeeNotification(TemplateView):
	template_name=('mysite/employee-dashboard/employee-notification.html')
	def get_context_data(self, *args, **kwargs):
		context = super(EmployeeNotification, self).get_context_data(*args, **kwargs)
		check_id = self.request.session['_auth_user_id']
		print(check_id)
		obj = StudentEmployeeNotification.objects.filter(sending_ids_id=int(check_id),pending=True)
		print('hellll')
		print(obj)
		if obj:
			context['notification'] = obj

		print('context:',context)

		return context

class EmployeeSearchStudent(TemplateView):
	template_name =('mysite/employee-dashboard/employee-search-existing-student.html')
	def get_context_data(self,*args,**kwargs):
		context = super(EmployeeSearchStudent, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])

		return context

	def post(self,request):
		print('in post result ')
		print('data:',request.POST)
		search = request.POST.get('search')
		logged_id = request.POST.get('logged_id')
		remove = []
		response_list = []
		skills_ids = list(Students.objects.filter(skills_interested__name__icontains=str(search)).values_list('username_id',flat=True))
		industry_ids = list(Students.objects.filter(industry_interested__name__icontains=str(search)).values_list('username_id',flat=True))


		if skills_ids and industry_ids:
			print('both found.')
			skills_ids = set(skills_ids)
			industry_ids = set(industry_ids)
			combine_ids = skills_ids | industry_ids
			final_ids = list(combine_ids)
			connected_ids = list(EmployeeStudentMapping.objects.filter(employee_user_id_id=int(logged_id)).values_list('connected_student_user_id_id',flat=True))
			print('connected_ids',connected_ids)
			print('final_ids',final_ids)
			if connected_ids:
				for i in final_ids:
					if i in connected_ids:
						remove.append(i)
				if remove :
					for k in remove:
						final_ids.remove(k)

			remove1 =[]

			if final_ids:
				pending_notification_ids = list(StudentEmployeeNotification.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_ids_id',flat=True))
				if pending_notification_ids:
					print('pending_ids:',pending_notification_ids)
					for i in final_ids:
						if i in pending_notification_ids:
							remove1.append(i)

					if remove1:
						for k in remove1:
							final_ids.remove(k)


			if final_ids:
				for i in final_ids:
					obj = Students.objects.filter(username_id=int(i)).first()
					if obj:
						context = {}
						context['first_name'] = obj.first_name
						context['surname'] = obj.surname
						context['skills_interested'] = obj.skills_interested.name
						context['industry_interested'] = obj.industry_interested.name
						context['username_id'] = obj.username.id
						context['logged_id'] = logged_id
						response_list.append(context)	

				return HttpResponse(json.dumps(response_list))
			else:
				return HttpResponse('0')
			
		else:
			if skills_ids:
				print('only skills match found.')
				final_ids = skills_ids
				connected_ids = list(EmployeeStudentMapping.objects.filter(employee_user_id_id=int(logged_id)).values_list('connected_student_user_id_id',flat=True))
				print('connected_ids',connected_ids)
				print('final_ids',final_ids)
				if connected_ids:
					for i in final_ids:
						if i in connected_ids:
							remove.append(i)
					if remove :
						for k in remove:
							final_ids.remove(k)

				remove1 =[]

				if final_ids:
					pending_notification_ids = list(StudentEmployeeNotification.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_ids_id',flat=True))
					if pending_notification_ids:
						print('pending_ids:',pending_notification_ids)
						for i in final_ids:
							if i in pending_notification_ids:
								remove1.append(i)

						if remove1:
							for k in remove1:
								final_ids.remove(k)

					if final_ids:
						for i in final_ids:
							obj = Students.objects.filter(username_id=int(i)).first()
							if obj:
								context = {}
								context['first_name'] = obj.first_name
								context['surname'] = obj.surname
								context['skills_interested'] = obj.skills_interested.name
								context['industry_interested'] = obj.industry_interested.name
								context['username_id'] = obj.username.id
								context['logged_id'] = logged_id

								response_list.append(context)	

						return HttpResponse(json.dumps(response_list))
					else:
						return HttpResponse('0')

			elif industry_ids:
				print('only industry match found.')
				final_ids = industry_ids
				connected_ids = list(EmployeeStudentMapping.objects.filter(employee_user_id_id=int(logged_id)).values_list('connected_student_user_id_id',flat=True))
				print('connected_ids',connected_ids)
				print('final_ids',final_ids)
				if connected_ids:
					for i in final_ids:
						if i in connected_ids:
							remove.append(i)
					if remove :
						for k in remove:
							final_ids.remove(k)


				remove1 =[]

				if final_ids:
					pending_notification_ids = list(StudentEmployeeNotification.objects.filter(logged_id_id=int(logged_id),pending=True).values_list('sending_ids_id',flat=True))
					if pending_notification_ids:
						print('pending_ids:',pending_notification_ids)
						for i in final_ids:
							if i in pending_notification_ids:
								remove1.append(i)

						if remove1:
							for k in remove1:
								final_ids.remove(k)


				if final_ids:
					for i in final_ids:
						obj = Students.objects.filter(username_id=int(i)).first()
						if obj:
							context = {}
							context['first_name'] = obj.first_name
							context['surname'] = obj.surname
							context['skills_interested'] = obj.skills_interested.name
							context['industry_interested'] = obj.industry_interested.name
							context['username_id'] = obj.username.id
							context['logged_id'] = logged_id

							response_list.append(context)

					return HttpResponse(json.dumps(response_list))
				else:
					return HttpResponse('0')
			else:
				print('not found.')
				return HttpResponse('0')

def student_employee_create_notification(request,id1,id2):
	if request.method == 'GET':
		print('dffgsgsgfs')
		print('logged_id',id1)
		print('username_id',id2)
		obj = StudentEmployeeNotification.objects.create(logged_id_id=int(id1),sending_ids_id=int(id2))
		obj.save()
		print('noti saved done.')
		return HttpResponse('0')
	else:
		return HttpResponse('1')

def student_employee_delete_notification(request,id1):
	if request.method == 'GET':
		print('notification_id',id1)
		obj = StudentEmployeeNotification.objects.filter(id=int(id1)).first()
		if obj:
			obj.delete()
			print('noti deleted.')
		return HttpResponse('0')
	else:
		return HttpResponse('1')

def student_employee_accept_notification(request,id1,id2):
	if request.method == 'GET':
		print('notification_id',id1)
		print('logged_id',id2)
		obj = Students.objects.filter(username_id=int(id2)).first()
		if obj:
			student_id = int(obj.id)
			print('accepter is future student.')
			obj1 = TeacherFutureNotifications.objects.filter(id=int(id1)).first()
			if obj1:
				obj1.pending = False
				obj1.save()
				print('pending status changed.')
				teacher_user_id = int(obj1.sending_ids_id)
				future_student_user_id = int(obj1.logged_id_id)
				print('student',student_user_id)
				print('to be connected teacher',teacher_user_id)
				print('obj for StudentEmployeeMapping')
				obj2 = StudentEmployeeMapping.objects.filter(student_user_id_id=int(student_user_id),connected_employee_user_id_id=int(connected_employee_user_id)).first()
				if obj2:
					print('already connected.1')
				else:
					obj3 = StudentEmployeeMapping.objects.create(student_user_id_id=int(student_user_id),connected_employee_user_id_id=int(connected_employee_user_id),student_id_id=inr(student_id))
					obj3.save()
					print('connection form student side added.')


				print('\n\n\n\n')
				employee_user_id = int(obj1.logged_id_id)
				ee_id = User_Info.objects.filter(username_id=int(employee_user_id)).first()
				employee_id = int(ee_id.id)
				connected_student_user_id = int(obj1.sending_ids_id)
				print('employee_user_id',employee_user_id)
				print('connected_student_user_id',connected_student_user_id)
				print('obj for EmployeeStudentMapping')
				obj4 = EmployeeStudentMapping.objects.filter(employee_user_id_id=int(employee_user_id),connected_student_user_id_id=int(connected_student_user_id)).first()
				if obj4:
					print('already connected.2')
				else:
					obj5 = EmployeeStudentMapping.objects.create(employee_user_id_id=int(employee_user_id),connected_student_user_id_id=int(connected_student_user_id),employee_id_id=int(employee_id))
					obj5.save()
					print('connection from employee side added.')

				return HttpResponse('0')


		ob2 = User_Info.objects.filter(username_id=int(id2)).first()
		if ob2:
			employee_id = int(ob2.id)
			print('accepter is employee')
			obj1 = StudentEmployeeNotification.objects.filter(id=int(id1)).first()
			if obj1:
				obj1.pending = False
				obj1.save()
				print('pending status changed.')
				employee_user_id = int(obj1.sending_ids_id)
				connected_student_user_id = int(obj1.logged_id_id)
				print('employee_user_id',employee_user_id)
				print('connected_student_user_id',connected_student_user_id)
				print('obj for EmployeeStudentMapping')
				obj2 = EmployeeStudentMapping.objects.filter(employee_user_id_id=int(employee_user_id),connected_student_user_id_id=int(connected_student_user_id)).first()
				if obj2:
					print('already connected 1.')
				else:
					obj3 = EmployeeStudentMapping.objects.create(employee_user_id_id=int(employee_user_id),connected_student_user_id_id=int(connected_student_user_id),employee_id_id=int(employee_id))
					obj3.save()
					print('connection from employee side added.')


				print('\n\n\n\n\n')
				student_user_id = int(obj1.logged_id_id)
				s_id = Students.objects.filter(username_id=int(student_user_id)).first()
				student_id = int(s_id.id)
				connected_employee_user_id = int(obj1.sending_ids_id)
				print('student_user_id',student_user_id)
				print('connected_employee_user_id',connected_employee_user_id)
				print('obj for StudentEmployeeMapping')
				obj4 = StudentEmployeeMapping.objects.filter(student_user_id_id=int(student_user_id),connected_employee_user_id_id=int(connected_employee_user_id)).first()
				if obj4:
					print('already connected 2.')
				else:
					obj5 = StudentEmployeeMapping.objects.create(student_user_id_id=int(student_user_id),connected_employee_user_id_id=int(connected_employee_user_id),student_id_id=int(student_id))
					obj5.save()
					print('connection form student side added.')

				return HttpResponse('0')


		print('in accept notification')
		return HttpResponse('0')
	else:
		return HttpResponse('1')

def student_employee_unfollow_notification(request,id1,id2):
	if request.method == 'GET':
		print('logged_id',id1)
		print('unlogged_id',id2)
		logged_id = id1
		unlogged_id = id2
		obj = Students.objects.filter(username_id=int(logged_id)).first()
		if obj:
			student_id = int(obj.id)
			print('doer is existing student.')
			student_user_id = int(logged_id)
			connected_employee_user_id = int(unlogged_id)
			print('student',student_user_id)
			print('to be connected employee',connected_employee_user_id)
			print('obj for StudentEmployeeMapping')
			obj2 = StudentEmployeeMapping.objects.filter(student_user_id_id=int(student_user_id),connected_employee_user_id_id=int(connected_employee_user_id)).first()
			if obj2:
				print('exist to unfollow')
				obj2.delete()
				print('connection deleted when doer is existing student.1')
			else:
				print('no connection is there to unfollow between employee and exsiting student.1')

			print('done 1.')


			print('\n\n\n\n\n')
			employee_user_id = int(unlogged_id)
			s_id = User_Info.objects.filter(username_id=int(unlogged_id)).first()
			employee_id = int(s_id.id)
			connected_student_user_id = int(logged_id)
			print('student_user_id',student_user_id)
			print('connected_employee_user_id',connected_employee_user_id)
			print('obj for EmployeeStudentMapping')
			obj4 = EmployeeStudentMapping.objects.filter(employee_user_id_id=int(employee_user_id),connected_student_user_id_id=int(connected_student_user_id)).first()
			if obj4:
				obj4.delete()
				print('connection deleted from employee side when the doer existing student.2')
				return HttpResponse('0')
			else:
				print('no connection is there to unfollow between employee and exsiting student.2')

			return HttpResponse('0')


		ob2 = User_Info.objects.filter(username_id=int(logged_id)).first()
		if ob2:
			employee_id = int(ob2.id)
			print('doer is employee')
			employee_user_id = int(logged_id)
			connected_student_user_id = int(unlogged_id)
			print('employee_user_id',employee_user_id)
			print('connected_student_user_id',connected_student_user_id)
			print('obj for EmployeeStudentMapping')
			obj3 = EmployeeStudentMapping.objects.filter(employee_user_id_id=int(employee_user_id),connected_student_user_id_id=int(connected_student_user_id)).first()
			if obj3:
				print('exist to unfollow')
				obj3.delete()
				print('connection deleted when doer is employee.3')
			else:
				print('no connection is there to unfollow between employee and exsiting student.3')

			print('done 2.')

			print('\n\n\n\n\n')
			student_user_id = int(unlogged_id)
			s_id = Students.objects.filter(username_id=int(unlogged_id)).first()
			student_id = int(s_id.id)
			connected_employee_user_id = int(logged_id)
			print('student_user_id',student_user_id)
			print('connected_employee_user_id',connected_employee_user_id)
			print('obj for StudentEmployeeMapping')
			obj4 = StudentEmployeeMapping.objects.filter(student_user_id_id=int(student_user_id),connected_employee_user_id_id=int(connected_employee_user_id)).first()
			if obj4:
				print('exist to unfollow')
				obj4.delete()
				print('connection deleted when doer is employee.4')
				return HttpResponse('0')
			else:
				print('no connection is there to unfollow between employee and exsiting student.3')

			return HttpResponse('0')


		else:
			return HttpResponse('0')
	else:
		return HttpResponse('0')

class EmployeeStudentFollowing(TemplateView):
	template_name = ('mysite/employee-dashboard/employee-student-following.html')
	def get_context_data(self, *args, **kwargs):
		context = super(EmployeeStudentFollowing, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
		user_id = int(self.request.session['_auth_user_id'])
		response_list = []
		obj = EmployeeStudentMapping.objects.filter(employee_user_id_id=user_id).values_list('connected_student_user_id_id',flat=True)
		if obj:
			print(obj)
			for i in obj:
				obj1 =Students.objects.filter(username_id=int(i)).first()
				if obj1:
					context1={}
					context1['first_name'] = obj1.first_name
					context1['skills'] = obj1.skills_interested.name
					context1['industry'] = obj1.industry_interested.name
					context1['username_id'] = obj1.username.id
					response_list.append(context1)

			context['already_added'] = response_list
			print(context)

		return context

##############Employee#############################################




############ExistingEmployee#######################################

class ExistingEmployeeProfile(TemplateView):
	template_name=('mysite/existing-employee-dashboard/existing-employee-profile.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ExistingEmployeeProfile, self).get_context_data(*args, **kwargs)
		print('user_id:',self.request.session['_auth_user_id'])
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
		print("This is Technical Subject",obj)
		obj1 = Country.objects.all()
		context['technical_subject'] = obj
		context['country_info'] = obj1
		
		return context



	def post(self,request):
		print('in Entrepreneurs')
		email = request.POST.get('email')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		country = request.POST.get('country')
		technical_subject = request.POST.get('technical_subject')


		print('\n\n\n\n')
		print('DATA:',request.POST)



		# print(type(email))
		# print(type(password))
		# print(type(user_type))
		# print(type(first_name))
		# print(type(surname))
		# print(type(date_of_birth))
		# print(type(phone_number))
		# print(type(position_in_company))
		# print(type(working_years))
		# print(type(no_of_employees))
		# print(type(website_url))
		# print(type(address))
		# print(type(country))
		# print(type(company_registration_number))
		# print(type(skills))
		# print(type(industry))


		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = True
				user.is_staff = True
				user.save()
				print("TechnicalSubject:",technical_subject)
				user_info = Professor.objects.create(username_id=user.id,first_name=user.first_name,surname=surname,email=user.username,country_id=country, technical_subject_id = technical_subject)
				user_info.save()
				return HttpResponse('1')

			except Exception as e:
				print('user error is :',e)
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
				user = User.objects.create(username=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = True
				user.is_staff = True
				user.save()
				user_info = Employeeee.objects.create(username_id=user.id,first_name=user.first_name,email=user.username,surname=surname,technical_subject_id = technical_subject,country_id=country)
				user_info.save()
				return HttpResponse('1')

			except Exception as e:
				print('user error is :',e)
				return HttpResponse('2')

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
		print('in employee post')
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


		print('\n\n\n\n')
		print('Data:',request.POST)
		print(type(first_name))
		print(type(surname))
		print(type(date_of_birth))
		print(type(position_in_company))
		print(type(website_url))
		print(type(address))
		print(type(country))
		print(type(email))
		print(type(phone_number))
		print(type(company_registration_number))
		print(type(skills))
		print(type(industry))
		print(type(password))

		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = True
				user.is_staff = True
				user.save()
				print(user.id)
				print(type(user.id))
				user_info = ExistingEmployee.objects.create(username_id=user.id,first_name=user.first_name,surname=surname,date_of_birth=date_of_birth,email=user.username,position_in_company=position_in_company,website_url=website_url,address=address,country_id=int(country),phone_number=phone_number,company_registration_number=company_registration_number,skills_id=int(skills),industry_id=int(industry))
				user_info.save()
				return HttpResponse('1')

			except Exception as e:
				print('user errorrr is :',e)
				return HttpResponse('2')
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
				user = User.objects.create(username=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = True
				user.is_staff = True
				user.save()
				future_student_info = Graduate.objects.create(username_id=user.id,first_name=user.first_name,email=user.username,surname=surname,technical_subject_id = technical_subject,country_id=country)
				future_student_info.save()
				return HttpResponse('1')

			except Exception as e:
				print('user error is :',e)
				return HttpResponse('2')		
# Student Registration is used for Student Registration
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

	def post(self,request):
		print('in post')
		email = request.POST.get('email')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		surname = request.POST.get('surname')
		country = request.POST.get('country')
		technical_subject = request.POST.get('technical_subject')
		student_type = request.POST.get('student_type')


		print(country)
		print('\n\n\n\n\n')
		print('DATA:', request.POST)

		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = True
				user.is_staff = True
				user.save()
				student_info = Students.objects.create(username_id=user.id,first_name=user.first_name,email=user.username,surname=surname,country_id=int(country),technical_subject_id = int(technical_subject), student_type_id = int(student_type))
				student_info.save()
				return HttpResponse('1')
			except Exception as e:
				print('user error is :',e)
				return HttpResponse('2')

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
		print('in teacher')
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

		print('\n\n\n\n')
		print('Data:',request.POST)

		user = User.objects.filter(username=email)
		if user:
			return HttpResponse('0')
		else:
			try:
				user = User.objects.create(username=email)
				user.set_password(password)
				user.save()
				user.first_name = first_name
				user.is_active = True
				user.is_staff = True
				user.save()
				teacher_info = Teacher.objects.create(username_id=int(user.id),first_name=user.first_name,email=user.username,surname=surname,title_id=int(title),university_name=university_name,university_address=university_address,phone_number=phone_number,position_id=int(position),programme_title=programme_title,subject_area_id=int(subject_area))
				teacher_info.save()
				return HttpResponse('1')
			except Exception as e:
				print('user error is :',e)
				return HttpResponse('2')


######################Other Funtions########################

class Profile(TemplateView):
	template_name=('mysite/profile.html')

class Logout(TemplateView):
	template_name = ('mysite/login.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Logout, self).get_context_data(*args, **kwargs)
		print('request',self.request)
		if '_auth_user_id' in self.request.session:
			del self.request.session['_auth_user_id'] 
			print('done.')
		return context

class Login(TemplateView):
	template_name = ('mysite/login.html')
	def get_context_data(self, *args, **kwargs):
		context = super(Login, self).get_context_data(*args, **kwargs)
		return context 

	def post(self,request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user_type = request.POST.get('user_type')
		print('username:',username)
		print('password:',password)
		print('user_type:',user_type)
		user = authenticate(username=username, password=password)
		if user:
			if user.is_superuser == True:
				return HttpResponse('0')
			else:
				if user_type == "student":
					print("user_type :",user_type)
					obj = Students.objects.filter(username_id=int(user.id)).first()
					if obj:
						login(request, user)
						return HttpResponse('1')
					else:
						return HttpResponse('6')



				if user_type == "graduate":
					print("user_type :",user_type)
					obj = Graduate.objects.filter(username_id=int(user.id)).first()
					if obj:
						login(request, user)
						return HttpResponse('2')
					else:
						return HttpResponse('6')

				if user_type == "professor" :
					print("user_type :",user_type)
					obj = Professor.objects.filter(username_id=int(user.id)).first()
					print('this is obj', obj)
					if obj:
						login(request, user)
						print("This is professor ")
						return HttpResponse('3')
					else:
						return HttpResponse('6')


				if user_type == "employee":
					print("user_type :",user_type)
					obj = Employeeee.objects.filter(username_id=int(user.id)).first()
					
					if obj:
						login(request, user)
						return HttpResponse('4')
					else:
						return HttpResponse('6')

				

		else:
			return HttpResponse('7')

class ForgotPassword(TemplateView):
	template_name = ('mysite/forgot.html')
	def get_context_data(self, *args, **kwargs):
		context = super(ForgotPassword, self).get_context_data(*args, **kwargs)
		return context

	def post(self,request):
		username = request.POST.get('username')
		user = User.objects.filter(username=username).first()
		if user:
			newpass = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
			print('new pass:',newpass)
			user.set_password(newpass)
			user.save()
			print('saved new.')
			sender = 'itsmepython21@gmail.com'
			receiver = username
			message = 'Hello '+str(user.first_name)+ ' Your New Password is -' +str(newpass)
			try:
				server = smtplib.SMTP('smtp.gmail.com', 587)
				server.starttls()
				server.login('itsmepython21@gmail.com', 'esfera0143')
				msg = EmailMessage()
				msg.set_content(message)
				msg['Subject'] = 'NEW PASSWORD'
				msg['From'] = 'itsmepython21@gmail.com'
				msg['To'] = str(receiver)
				server.send_message(msg) 
				print('sent...')      
				return HttpResponse('1')
			except Exception as e:
				return HttpResponse('2')
		else:
			return HttpResponse('0')

######################Other Funtions########################





