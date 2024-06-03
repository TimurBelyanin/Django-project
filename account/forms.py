from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput

User = get_user_model()


class UserCreateForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['email'].label = 'Ваша почта'
		self.fields['email'].required = True
		self.fields['username'].help_text = ''
		self.fields['password1'].help_text = ''
		# self.fields['password2'].help_text = 'hi'

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		if User.objects.filter(email=email).exists() or len(email) > 254:
			raise forms.ValidationError('Email is already in use or too long!')
		return email


class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


class UserEditForm(forms.ModelForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['email'].label = 'Ваша почта'
		self.fields['email'].required = True
