from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # Importing the Profile model
from .models import Category  # Importing the Category model


class RegisterForm(UserCreationForm):  # Form for user registration
    email = forms.EmailField()  # Adding email field to collect user email

    class Meta:
        model = User  # Setting the model to Django's built-in User model
        fields = ['username', 'email', 'password1', 'password2']  # Defining the fields to be displayed


class ProfileForm(forms.ModelForm):  # Form for updating user profile details
    class Meta:
        model = Profile  # Associating the form with the Profile model
        fields = ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']  # Fields available in the form


class MealFilterForm(forms.Form):  # Form for filtering meals based on categories
    category_choices = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # Fetching all categories from the database
        required=False,  
        widget=forms.CheckboxSelectMultiple,  # Display categories as multiple checkboxes
        label="Filter by Categories"  # Label for this field in the template
    )

    sort_by = forms.CharField(
        required=False,  # Sorting is optional
        label="Sort by",  # Label for sorting
        widget=forms.HiddenInput()  # Hidden input field, as dropdown selection will be in the template
    )

    def __init__(self, *args, **kwargs):  # Custom initialization of the form
        super().__init__(*args, **kwargs)
        self.fields['category_choices'].queryset = Category.objects.all()  # Dynamically setting category choices