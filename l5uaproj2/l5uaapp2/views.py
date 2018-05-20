from django.shortcuts import render
from l5uaapp2.forms import UserForm,UserProfileInfoForm

#specific for logins
from django.urls import reverse	#django.core.urlresolvers is deprecated
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
	return render(request,"index.html")

#view for logout	

@login_required	#decorator which makes sure that the immediate next func is exec only if user is logged in 
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))
	
	
#view for registration page	
def register(request):
	
	registered = False
	
	if request.method == "POST":	#if submit button is clicked
		
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileInfoForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			
			user=user_form.save()	#save the form to db
			user.set_password(user.password)	#hashing the password
			user.save()	#saving the hashed password to the database
			
			profile=profile_form.save(commit=False)
			profile.user=user 	#setting the OneToOne relationship as per described in models.py
			
			if 'profile_pic' in request.FILES:	#if there is a key named profile_pic in the request files
				profile.profile_pic=request.FILES['profile_pic']	#save it as profile_pic for the profile by getting the value for key
				
			profile.save()
			
			registered = True
			
		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form=UserForm()	#if submit button not clicked, or request is not POST but it is HttpResponse, display userform and profileform
		profile_form=UserProfileInfoForm()

	#return registration.html we need value of registered, user_form and profile_form there. they are explained here
	return render(request,"registration.html",
							{"registered":registered,
							'user_form':user_form,
							'profile_form':profile_form})

#view for login and logout							
def user_login(request):
	
	if request.method == "POST":	#user clicked submit
		username=request.POST.get('username')	#we use get 'username' bcoz the username will be sent through url by value for username key labeled in login.html
		password=request.POST.get('password')
		
		user=authenticate(username=username,password=password)	#chks for user record in users of our db
		
		if user:	#user successfully authenticated by chking entry in db
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
			
			else:
				return HttpResponse("Account not active")
		else:
			return HttpResponse("Invalid User")
	else:
		return render(request,'login.html')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	