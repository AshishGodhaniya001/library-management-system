from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def register_student(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        enrollment_no = request.POST['enrollment_no']
        # TODO: validations
        user = User.objects.create_user(
            username=username,
            password=password,
            role='student',
            enrollment_no=enrollment_no
        )
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')
    return render(request, 'accounts/register.html')
