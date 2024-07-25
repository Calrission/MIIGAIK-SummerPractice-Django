from django import forms
from django.contrib.auth.models import User
from django.db.models import DecimalField
from django.forms import DateInput

from .models import Profile, Token


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def validation_password(self):
        password = self.data['password']
        confirm_password = self.data['password2']
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")
        return password

    def validation_email(self):
        data = self.data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def validation(self):
        self.validation_email()
        self.validation_password()

    def is_valid(self):
        self.validation()
        return super().is_valid()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    photo = forms.FileField(required=False)

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date', "required": False}),
        }


class TokenForm(forms.ModelForm):

    code = DecimalField(max_digits=6)

    class Meta:
        model = Token
        fields = ['code']
