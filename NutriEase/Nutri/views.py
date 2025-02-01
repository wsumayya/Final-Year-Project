from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import RegisterForm
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from .forms import MealFilterForm
from .models import Meal, Category, FavouriteMeal
from django.shortcuts import get_object_or_404
from .models import Comment

from django.contrib import messages
from django.db.models import Count
from datetime import datetime
# import matplotlib.pyplot as plt
from io import BytesIO
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum





def home(request):
    return render(request, 'home.html')  # This will render the 'home.html' template


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account has been created successfully!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

 


# Profile Update view
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('base')  # Redirect to the home after profile is updated
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to the URL name of your dashboard or homepage
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirects the user to the login page after logout

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Optionally, you can manually specify the domain instead of relying on get_current_site
            domain = '127.0.0.1:8000'  # Set your domain here for local development or use actual domain for production
            form.save(request=request)  # Form will send the email to reset password
    else:
        form = PasswordResetForm()

    return render(request, 'password-reset.html', {'form': form})



@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    try:
        # Get the user's profile if it exists, otherwise create a new one
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect the user to the meals page (front page)
            return redirect('meals')  # Make sure to replace 'meals' with your actual meals page URL name
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})




def meal_page(request):
    meals = Meal.objects.all()  # Fetch all meals from the database
    return render(request, 'meal_page.html', {'meals': meals})




@login_required
def base_view(request):
    return render(request, 'base.html')

    


def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    return render(request, 'meal-detail.html', {'meal': meal})




def meals_view(request):
    # Initialize the form with request.GET data
    form = MealFilterForm(request.GET or None)
    meals = Meal.objects.all()  # Get all meals initially

    # Apply category filter
    if form.is_valid():
        selected_categories = form.cleaned_data.get('category_choices')
        if selected_categories:
            meals = meals.filter(categories__in=selected_categories).distinct()

    # Sorting logic based on query parameters
    sort_by = request.GET.get('sort_by', '')  # Default to empty string to prevent None
    if sort_by == 'calories':
        meals = meals.order_by('calories')  # Sort by calories (ascending)
    elif sort_by == 'protein':
        meals = meals.order_by('-protein')  # Sort by protein (descending)
    elif sort_by == 'fibre':
        meals = meals.order_by('-fibre')  # Sort by fibre (descending)
    elif sort_by == 'low_fat':
        meals = meals.order_by('fats')  # Sort by fats (ascending)
    elif sort_by == 'low_carbs':
        meals = meals.order_by('carbs')  # Sort by carbs (ascending)

    context = {
        'form': form,
        'meals': meals,
    }
    return render(request, 'meals.html', context)







def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def comments(request):
    # Fetch all comments from the database
    all_comments = Comment.objects.filter(parent__isnull=True).order_by('-created_at')

    if request.method == 'POST':
        # Handle new comment creation
        user_comment = request.POST.get('comment')
        parent_id = request.POST.get('parent_id') 
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

        
        if user_comment:
            Comment.objects.create(content=user_comment, user=request.user, parent=parent)
            return redirect('comments')  # Redirect to the same page after posting a comment

    return render(request, 'comment.html', {'comments': all_comments})




@login_required
def add_to_favourites(request, meal_id):
    """Allows users to add meals to their favourites"""
    meal = get_object_or_404(Meal, id=meal_id)
    FavouriteMeal.objects.create(user=request.user, meal=meal)  # Add to favourites
    return redirect('favourite')  # Redirect to favourites page

@login_required
def favourites_list(request):
    """Displays all the meals a user has favourited"""
    favourite_meals = FavouriteMeal.objects.filter(user=request.user).order_by('-added_at')
    return render(request, "favourite.html", {"favourite_meals": favourite_meals})

@login_required
def meal_detail(request, meal_id):
    """Displays the details of a selected favourite meal"""
    meal = get_object_or_404(Meal, id=meal_id)
    return render(request, "meal-detail.html", {"meal": meal})

@login_required
def remove_from_favourites(request, meal_id):
    """Removes a meal from the user's favourites"""
    meal = get_object_or_404(Meal, id=meal_id)
    FavouriteMeal.objects.filter(user=request.user, meal=meal).delete()
    return redirect('favourite')