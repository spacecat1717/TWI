from django import forms
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    """Form for Registering new users"""
    email = forms.EmailField(max_length=100)
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

class AccountAuthenticationForm(forms.ModelForm):
    """Form for Logging in  users"""
    password = forms.CharField(label = 'Пароль', widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ('email', 'password')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Неверный email')
                

class AccountUpdateForm(forms.ModelForm):
    """ Updating User Info"""
    class Meta:
        model = Account
        fields = ('email', 'username')
        widgets = {
                   'email':forms.TextInput(attrs={'class':'form-control'}),
                   'password':forms.TextInput(attrs={'class':'form-control'}),
        }
    def clean_email(self):
        #check unique for email
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk = self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email '%s' уже используется" %email)

    def clean_username(self):
        #check unique for username
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk = self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("Логин '%s' уже используется" % username)