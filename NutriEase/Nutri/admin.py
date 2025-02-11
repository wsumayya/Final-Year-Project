from django.contrib import admin
from .models import Meal, Category, Comment, FavouriteMeal, Profile  

# Register the Category model with custom admin settings
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name of the category in the admin list view
    search_fields = ('name',)  # Enable search functionality by category name





# Register the Meal model with custom admin settings
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories')  # Show meal name and calorie count in the list view
    list_filter = ('categories',)  # Enable filtering meals by categories in the admin panel
    search_fields = ('name', 'description')  # Allow searching meals by name or description
    filter_horizontal = ('categories',)  # Use a horizontal widget for Many-to-Many fields






# Register the Comment model with custom admin settings
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'created_at', 'parent')  # Display comment details in list view
    search_fields = ('content', 'user__username')  # Enable search by content and username
    list_filter = ('created_at',)  # Allow filtering by comment creation date





# Register the Profile model with custom admin settings
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'height', 'age', 'gender', 'activity_level', 'goal')  # Display profile details
    search_fields = ('user__username', 'user__first_name', 'user__last_name')  # Allow search by username and name





# Register the FavouriteMeal model with custom admin settings
@admin.register(FavouriteMeal)
class FavouriteMealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal', 'added_at')  # Show user, meal, and the date it was added
    search_fields = ('user__username', 'meal__name')  # Allow searching by username and meal name
    list_filter = ('added_at',)  # Enable filtering by date meal was added to favourites