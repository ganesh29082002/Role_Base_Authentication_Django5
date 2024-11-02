from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def register_view(request):
    if request.user.is_authenticated:
        # Redirect to dashboard if already logged in
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        # Redirect to dashboard if already logged in
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator

@role_required(['admin'])
@login_required
def manage_users_view(request):
    return render(request, 'manage_users.html')

def logout_view(request):
    logout(request)
    return redirect('login')
