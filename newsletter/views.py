from django.shortcuts import render

# Create your views here. 
from django.conf import settings
from .forms import SignUpForm, ContactForm
from django.core.mail import send_mail
from .models import SignUp

def home(request):
	title = "Sign Up Now"
	# if request.user.is_authenticated():
	# 	title = "My %s" % (request.user)
	# if request.method == "POST":
	# 	print request.POST
	form = SignUpForm(request.POST or None)
	context = {
		"title" : title,
		"form" : form
	}
	if form.is_valid():
		# form.save()
		instance = form.save(commit=False)
		# if not instance.full_name:
		# 	instance.full_name = "User"
		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "New Full Name"
		instance.full_name = full_name
		instance.save()
		context = {
		"title" : "Thank You!"
		}
	if request.user.is_authenticated() and request.user.is_staff:
		# i =1
		# for instance in SignUp.objects.all():
		# 	print instance.full_name	 , "%s" % str(i)
		# 	i += 1

		context = {
			"queryset" :SignUp.objects.all().order_by("-timestamp")
		}

	return render(request, "home.html", context)

def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():

		#method one for accessing data form
		# for key, value in form.cleaned_data.iteritems():
		# 	print key , value

		#Method two to access
		# for key in form.cleaned_data:
		# 	print key +" : " + form.cleaned_data.get(key)

		#Method three to access
		email = form.cleaned_data.get("email")
		message = form.cleaned_data.get("message")
		full_name = form.cleaned_data.get("full_name")
		# print email, message, full_name
		subject = "Site Conttact Form"
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email]
		some_html_message = """ 
			<h1> Hello there </h1>
			""" 
		contact_messsage =" %s : %s via %s " % (full_name, message, email)

		send_mail(subject,contact_messsage,
			 from_email,to_email, html_message=some_html_message,
			  fail_silently=False )
	context = {
		 "form" : form,
	}
	return render(request, "forms.html", context)

	