from django.db import models
from django.contrib.auth.models import User




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    calories = models.PositiveIntegerField(default=0)  # ✅ Added default
    protein = models.FloatField(default=0.0)  # ✅ Added default
    carbs = models.FloatField(default=0.0)  # ✅ Added default
    fats = models.FloatField(default=0.0)  # ✅ Added default
    fibre = models.FloatField(default=0.0)  # ✅ Added default
    image = models.ImageField(upload_to='meal_images/', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    ingredients = models.TextField(default="", blank=True)  # ✅ Set default to empty string
    instructions = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=70)  # Add a default value
    height = models.IntegerField(default=170)  # Default height set
    age = models.IntegerField(null=False, default=25)  # Example default value
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')],
    default='Female')
    activity_level = models.CharField(
    max_length=20,
    null=False,
    blank=True,
    default='Sedentary',
    choices=[  # Missing comma before `choices`
        ('Sedentary', 'Sedentary'),
        ('Moderate', 'Moderate'),
        ('Active', 'Active'),
    ]
)

    goal = models.CharField(
    max_length=50,
    choices=[('Lose Weight', 'Lose Weight'), ('Gain Muscle', 'Gain Muscle'), ('Maintain Weight', 'Maintain Weight')],
    default='Maintain Weight'
)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank = True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.content[:50]