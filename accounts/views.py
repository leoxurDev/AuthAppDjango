from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Profile, PortfolioImage
from accounts.forms import ProfileForm, PortfolioImageForm

def home(request):
    # Fetch active public profiles to display on the landing page (exclude private profiles)
    featured_profiles = Profile.objects.filter(user__is_active=True, is_private=False).exclude(user__username='admin').order_by('?')[:6]
    return render(request, 'home.html', {
        'user': request.user,
        'featured_profiles': featured_profiles
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return render(request, 'login.html', {'error': 'This account has been deactivated. Please contact support.'})
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Account created successfully! Welcome to your dashboard.")
        return redirect('dashboard')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'submit_profile' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            project_form = PortfolioImageForm()
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Error updating profile. Please check the fields below.")
        elif 'submit_project' in request.POST:
            profile_form = ProfileForm(instance=profile)
            project_form = PortfolioImageForm(request.POST, request.FILES)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.profile = profile
                project.save()
                messages.success(request, "Portfolio item added successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Error adding portfolio item. Ensure you selected a valid image.")
    else:
        profile_form = ProfileForm(instance=profile)
        project_form = PortfolioImageForm()
        
    projects = profile.images.all().order_by('-created_at')
    
    return render(request, 'dashboard.html', {
        'profile': profile,
        'profile_form': profile_form,
        'project_form': project_form,
        'projects': projects
    })

@login_required
def delete_portfolio_item(request, project_id):
    profile = get_object_or_404(Profile, user=request.user)
    project = get_object_or_404(PortfolioImage, id=project_id, profile=profile)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Portfolio item deleted successfully.")
    return redirect('dashboard')

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    if not user.is_active:
        return render(request, '404.html', {'message': 'This profile is currently inactive.'}, status=404)
        
    profile, created = Profile.objects.get_or_create(user=user)
    projects = profile.images.all().order_by('-created_at')
    
    is_owner = request.user.is_authenticated and request.user == user
    is_private_locked = profile.is_private and not is_owner
    
    return render(request, 'profile_view.html', {
        'profile': profile,
        'projects': projects,
        'show_edit_link': is_owner,
        'is_private_locked': is_private_locked,
        'is_preview_private': profile.is_private and is_owner
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        # User is not staff, show forbidden page or redirect
        return render(request, '403.html', status=403)
        
    users = User.objects.all().order_by('-date_joined')
    active_count = users.filter(is_active=True).count()
    staff_count = users.filter(is_staff=True).count()
    
    return render(request, 'admin_dashboard.html', {
        'users': users,
        'active_count': active_count,
        'staff_count': staff_count
    })

@login_required
def admin_toggle_status(request, user_id):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
        
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
    else:
        target_user.is_active = not target_user.is_active
        target_user.save()
        status_str = "activated" if target_user.is_active else "deactivated"
        messages.success(request, f"User {target_user.username} has been {status_str}.")
        
    return redirect('admin_dashboard')

@login_required
def admin_toggle_role(request, user_id):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
        
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot change your own staff status.")
    else:
        target_user.is_staff = not target_user.is_staff
        target_user.save()
        role_str = "granted Staff access" if target_user.is_staff else "revoked Staff access"
        messages.success(request, f"User {target_user.username} has been {role_str}.")
        
    return redirect('admin_dashboard')

@login_required
def admin_delete_user(request, user_id):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
        
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot delete your own account.")
    elif request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f"User account '{username}' has been permanently deleted.")
        
    return redirect('admin_dashboard')
