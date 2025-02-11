from django.contrib import admin
from django.urls import path
from Nutri import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from Nutri.views import (
    add_to_favourites, favourites_list, meal_detail, remove_from_favourites
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('base/', views.base_view, name='base'),  
    path('password-reset/', views.password_reset_view, name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('meals/', views.meals_view, name='meals'),
    path('meal/<int:meal_id>/', views.meal_detail, name='meal_detail'),  
    path('comments/', views.comments, name='comments'),
    path('favourite-meal/<int:meal_id>/', add_to_favourites, name='add_to_favourites'),
    path('favourite/', favourites_list, name='favourite'), 
    path('meal/<int:meal_id>/', meal_detail, name='meal_detail'),
    path('meals/', views.meals_view, name='meal_list'), 
    path('remove-favourite/<int:meal_id>/', remove_from_favourites, name='remove_from_favourites'),
]

   

     
if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)