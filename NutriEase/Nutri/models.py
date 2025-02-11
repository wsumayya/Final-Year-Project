from django.db import models
from django.contrib.auth.models import User  # Importing Django's built-in User model


# Category Model: Represents meal categories (e.g., Vegan, High Protein)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Category name must be unique

    def __str__(self):
        return self.name  # String representation of the model


# Meal Model: Represents individual meals with nutritional information
class Meal(models.Model):
    name = models.CharField(max_length=255)  # Meal name
    description = models.TextField()  # Meal description
    calories = models.PositiveIntegerField(default=0)  # Number of calories in the meal
    protein = models.FloatField(default=0.0)  # Protein content in grams
    carbs = models.FloatField(default=0.0)  # Carbohydrate content in grams
    fats = models.FloatField(default=0.0)  # Fat content in grams
    fibre = models.FloatField(default=0.0)  # Fibre content in grams
    image = models.ImageField(upload_to='meal_images/', blank=True, null=True)  # Optional image for the meal
    categories = models.ManyToManyField(Category, blank=True)  # Many-to-Many relation with Category
    ingredients = models.TextField(default="", blank=True)  # Ingredients list as text
    instructions = models.TextField(default="", blank=True)  # Cooking instructions as text

    def __str__(self):
        return self.name  # String representation of the model


# Profile Model: Stores additional user details such as weight, height, age, etc.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One relation with User model
    weight = models.IntegerField(default=70)  # Default weight in kg
    height = models.IntegerField(default=170)  # Default height in cm
    age = models.IntegerField(null=False, default=25)  # User's age
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        default='Female'  # Default gender is Female
    )
    activity_level = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        default='Sedentary',  # Default activity level is Sedentary
        choices=[
            ('Sedentary', 'Sedentary'),
            ('Moderate', 'Moderate'),
            ('Active', 'Active'),
        ]
    )
    goal = models.CharField(
        max_length=50,
        choices=[
            ('Lose Weight', 'Lose Weight'),
            ('Gain Muscle', 'Gain Muscle'),
            ('Maintain Weight', 'Maintain Weight'),
        ],
        default='Maintain Weight'  # Default goal is to maintain weight
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"  # String representation of the model


# Comment Model: Represents user comments and allows nested replies
class Comment(models.Model):
    content = models.TextField()  # Comment text content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment is created
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # User who posted the comment
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )  # Parent comment for nested replies

    def __str__(self):
        return self.content[:50]  


# FavouriteMeal Model: Allows users to favourite meals
class FavouriteMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who favourited the meal
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)  # The meal being favourited
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when it was added to favourites

    def __str__(self):
        return f"{self.user.username} - {self.meal.name}"  # String representation of the model