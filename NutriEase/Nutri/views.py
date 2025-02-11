from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils.timezone import now
from datetime import datetime, timedelta
from io import BytesIO

from .forms import RegisterForm, ProfileForm, MealFilterForm
from .models import Profile, Meal, Category, FavouriteMeal, Comment

# Home Page View
def index(request):
    return render(request, 'index.html')  # This will render the 'home.html' template

# User Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account has been created successfully!')
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Profile Update View
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('base')  # Redirect to home after profile is updated
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirect to login page after logout

# Password Reset View
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            domain = '127.0.0.1:8000'  
            form.save(request=request)  # Sends email for password reset
    else:
        form = PasswordResetForm()
    return render(request, 'password-reset.html', {'form': form})

# User Profile View
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create user profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Save profile updates
            return redirect('meals')  # Redirect to meals page
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

# Meal Page View
def meal_page(request):
    meals = Meal.objects.all()  # Fetch all meals from the database
    return render(request, 'meal_page.html', {'meals': meals})

# Base View
@login_required
def base_view(request):
    return render(request, 'base.html')

# Meal Detail View
def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)  # Retrieve meal 
    return render(request, 'meal-detail.html', {'meal': meal})

# Meal Filtering and Sorting View
def meals_view(request):
    form = MealFilterForm(request.GET or None)  # Initialize form with GET data
    meals = Meal.objects.all()  # Fetch all meals 

    # Apply category filter if selected
    if form.is_valid():
        selected_categories = form.cleaned_data.get('category_choices')
        if selected_categories:
            meals = meals.filter(categories__in=selected_categories).distinct()

    # Sorting logic based on user selection
    sort_by = request.GET.get('sort_by', '')  
    if sort_by == 'calories':
        meals = meals.order_by('calories')  # Sort by calories ascending
    elif sort_by == 'protein':
        meals = meals.order_by('-protein')  # Sort by protein descending
    elif sort_by == 'fibre':
        meals = meals.order_by('-fibre')  # Sort by fibre descending
    elif sort_by == 'low_fat':
        meals = meals.order_by('fats')  # Sort by fats ascending
    elif sort_by == 'low_carbs':
        meals = meals.order_by('carbs')  # Sort by carbs ascending

    context = {
        'form': form,
        'meals': meals,
    }
    return render(request, 'meals.html', context)

# Comments View
@login_required
def comments(request):
    all_comments = Comment.objects.filter(parent__isnull=True).order_by('-created_at')  # Fetch all top-level comments

    if request.method == 'POST':
        user_comment = request.POST.get('comment')
        parent_id = request.POST.get('parent_id') 
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

        if user_comment:
            Comment.objects.create(content=user_comment, user=request.user, parent=parent)  # Save new comment
            return redirect('comments')  # Redirect to comments page

    return render(request, 'comment.html', {'comments': all_comments})

# Add Meal to Favourites
@login_required
def add_to_favourites(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)  # Get meal 
    FavouriteMeal.objects.create(user=request.user, meal=meal)  # Add to favourites
    return redirect('favourite')  # Redirect to favourites page

# List Favourited Meals
@login_required
def favourites_list(request):
    favourite_meals = FavouriteMeal.objects.filter(user=request.user).order_by('-added_at')  # Fetch all favourited meals
    return render(request, "favourite.html", {"favourite_meals": favourite_meals})

# Favourite Meal Detail View
@login_required
def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)  # Retrieve favourite meal details
    return render(request, "meal-detail.html", {"meal": meal})

# Remove Meal from Favourites
@login_required
def remove_from_favourites(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)  # Retrieve meal
    FavouriteMeal.objects.filter(user=request.user, meal=meal).delete()  # Remove from favourites
    return redirect('favourite')  # Redirect to favourites page