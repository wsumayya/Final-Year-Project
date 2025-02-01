
from django.contrib import admin
from .models import Meal, Category, Comment, FavouriteMeal
from .models import Profile
from .models import Meal  # ✅ Only import Meal


# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name of the category in the admin list view
    search_fields = ('name',)  # Allow searching by category name

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories')  # Show name and calories in the admin list view
    list_filter = ('categories',)  # Filter meals by categories in the admin panel
    search_fields = ('name', 'description')  # Allow searching meals by name or description
    filter_horizontal = ('categories',)  # Use a horizontal widget for Many-to-Many fields



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'created_at', 'parent') 
    search_fields = ('content', 'user__username')
    list_filter = ('created_at',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'height', 'age', 'gender', 'activity_level', 'goal')  # Removed extra comma
    search_fields = ('user__username', 'user__first_name', 'user__last_name')  # Correct field references




@admin.register(FavouriteMeal)
class FavouriteMealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal', 'added_at')  # Show user, meal, and date added
    search_fields = ('user__username', 'meal__name')  # Allow searching by user and meal name
    list_filter = ('added_at',)  # Filter by date added