from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Category


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']


class MealFilterForm(forms.Form):
    category_choices = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Filter by Categories"
    )

    sort_by = forms.CharField(
        required=False,
        label="Sort by",
        widget=forms.HiddenInput()  # Hidden input, dropdown will be in the template
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_choices'].queryset = Category.objects.all()