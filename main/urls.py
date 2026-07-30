# my_project/urls.py (Your main project configuration folder)

from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is imported
from django.contrib.auth import views as auth_views
from Store import views as store_views # Imports views from your Store app

urlpatterns = [
    # 1. KEEP YOUR OLD ADMIN ROUTE (The one showing in your screen snapshot)
    path('admin/', admin.site.urls),
    
    # 2. ADD THE NEW AUTHENTICATION ROUTES BELOW IT
    path('register/', store_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
]
