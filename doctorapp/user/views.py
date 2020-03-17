# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages 
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from .forms import UserRegisterForm 
from django.core.mail import send_mail,EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage

def index(request):
	user = request.user
	num_items_in_cart=user.profile.cart_items.all().count()
	return render(request, 'home/navbar.html',{'num_items_in_cart':num_items_in_cart})


def activation_sent_view(request):
    return render(request, 'user/activation_sent.html')

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	print(account_activation_token.check_token(user, token))
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.signup_confirmation = True
		user.save()
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		return redirect('home:landing')
	else:
		return render(request, 'user/activation_invalid.html')


def register(request): 
	if request.method == 'POST':	
		form = UserRegisterForm(request.POST)
		print(form)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.email = form.cleaned_data.get('email')
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Please activate your Account'
			message = render_to_string('user/activation_request.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			print(message)
			email = EmailMessage('email_subject', message, to=[user.profile.email])
			email.send()
			messages.success(request, "Your account has been created ! You are now able to log in")
			return redirect('user:activation_sent')
	else: 
		form = UserRegisterForm()
	return render(request, 'user/login_page_1.html', {'form': form, 'title':'reqister here'}) 


def Login(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password1')
		print(username)
		print(password)
		user=authenticate(request, username=username, password=password)
		print(user)
		if user is not None:
			form=login(request, user)
			messages.success(request, f'Welcome {username} !!')
			user = request.user
			user.save()
			# print(user.profile.bio)
			return redirect('home:landing')
		else:
			messages.info(request, f'Account done, please login')
	form=AuthenticationForm()

	return render(request, 'home/landingpage.html', {'form':form, 'title':'log in','user':user})

def profilepage(request):
	user=request.user
	all_items = user.profile.cart_items.all()
	print(all_items)
	return render(request, 'user/profile.html', {'all_items':all_items})