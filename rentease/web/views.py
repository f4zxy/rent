from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User  # Import your custom User model
from django.template import loader

# Home Page
def ok(request):
    return render(request, "web/home.html")

# Register User
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required!")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                admin_type='CUSTOM'  # Default admin type
            )
            messages.success(request, "Registration successful! Please login.")
            return redirect('user_login')
            
    return render(request, 'web/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            messages.error(request, "Username and Password are required!")
            return render(request, 'web/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['onpro'] = user.username  # Set session variable
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Redirect to home page after login
            return redirect('home')  # Make sure 'home' is defined in urls.py
        else:
            messages.error(request, "Invalid credentials!")
    
    return render(request, 'web/login.html')
# Admin Dashboard
@login_required
@user_passes_test(lambda u: u.admin_type in ['SUPER', 'STAFF', 'CUSTOM'])
def admin_dashboard(request):
    return render(request, 'admin/custom_dashboard.html')

# Profile Page
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        
        # Handle password change securely
        new_password = request.POST.get('new_password')
        if new_password:
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters")
            else:
                user.set_password(new_password)
                messages.success(request, "Password updated successfully!")
        
        user.save()
        messages.success(request, "Profile updated!")
        return redirect('profile')
    
    return render(request, 'web/edit_profile.html', {'user': user})

# Logout
def logout_view(request):

    return render(request, "web/home.html")