from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm
from .models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Profile.objects.create(
                user=user,
                role=profile_form.cleaned_data['role'],
                bio=profile_form.cleaned_data['bio']
            )
            return redirect('accounts:login')
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    return render(request, 'accounts/dashboard.html', {'profile': profile})


@login_required
def logout_view(request):
    logout(request)
    return redirect('courses:course_list')