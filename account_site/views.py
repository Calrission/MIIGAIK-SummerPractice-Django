from django.contrib.auth.models import User
from random import randint
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm, TokenForm
from .models import Profile, Token
from django.conf import settings
from django.core.mail import send_mail


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Disabled account_site')
            else:
                messages.error(request, 'Invalid login')
    else:
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        try:
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.data['password'])
                new_user.save()
                code = randint(100000, 999999)
                Token(user=new_user, code=code).save()
                Profile.objects.create(user=new_user)
                subject = 'Welcome to my blog'
                message = f'Hi {user_form.data["first_name"]}, thank you code: {code}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_form.data["email"]]
                send_mail(subject, message, email_from, recipient_list)
                return render(request,
                              'account/register_code.html',
                              {'new_user': new_user, 'form': TokenForm()})
        except ValidationError as e:
            messages.error(request, e.message)
    user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_db = User.objects.get(pk=request.user.id)
        user_form = UserEditForm(request.POST, instance=user_db)
        profile_db = Profile.objects.get(user=request.user)
        profile_form = ProfileEditForm(request.POST, instance=profile_db, files=request.FILES)
        valid = [False, False]
        if user_form.is_valid():
            user_form.save()
            valid[0] = True
        if profile_form.is_valid():
            profile_form.save()
            valid[1] = True
        if any(valid):
            messages.success(request, 'Your account has been updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserEditForm(instance=request.user)
        if not request.user.is_superuser:
            profile = Profile.objects.get(user_id=request.user.id)
        else:
            profile = None
        profile_form = ProfileEditForm(instance=profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


def redirect_vk(request):
    pass


def code(request):
    if request.method == "POST":
        token_db = Token.active_objects.get(code=request.POST['code'])
        form = TokenForm(request.POST, instance=token_db)
        if form.is_valid():
            token = form.save(commit=False)
            token.active = False
            token.save()
            return redirect("account_site:login")
        else:
            messages.error(request, 'Invalid code')
            return
    return redirect("/")
