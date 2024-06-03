from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email
from .forms import UserCreateForm, LoginForm, UserEditForm


User = get_user_model()


# def email_verification(request):
# 	return render(request, 'account/email/email_verification_sent.html')


def register_user(request):
	if request.method == "POST":
		form = UserCreateForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user_email = form.cleaned_data['email']
			user_name = form.cleaned_data['username']
			user_password = form.cleaned_data['password1']

			# Create new user
			user = User.objects.create_user(username=user_name, email=user_email, password=user_password)
			user.is_active = False

			send_email(user)

			return redirect('account:email-verification-sent')
	else:
		form = UserCreateForm()
	return render(request, 'account/registration/register.html', {'form': form})


def login_user(request):
	form = LoginForm()

	if request.user.is_authenticated:
		print('kek')
		return redirect('shop:products')

	if request.method == 'POST':

		form = LoginForm(request.POST)

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('account:dashboard')
		else:
			messages.info(request, 'Username or Password is incorrect')
			return redirect('account:login')
	context = {
		'form': form
	}
	return render(request, 'account/login/login.html', context)


def logout_user(request):
	logout(request)
	return redirect('shop:products')


@login_required(login_url='account:login')
def dashboard(request):
	return render(request, 'account/dashboard/dashboard.html')


@login_required(login_url='account:login')
def profile_user(request):
	if request.method == 'POST':
		form = UserEditForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect('account:dashboard')
	else:
		form = UserEditForm(instance=request.user)
	context = {'form': form}
	return render(request, 'account/dashboard/profile.html', context)


@login_required(login_url='account:login')
def delete_user(request):
	user = User.objects.get(id=request.user.id)
	if request.method == 'POST':
		user.delete()
		return redirect('shop:products')
	return render(request, 'account/dashboard/account_deleted.html')
