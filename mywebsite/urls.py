from django.contrib import admin
from django.urls import path, include  
from django.contrib.auth import views as auth_views
from store import views as store_views # 👈 CHANGED TO LOWERCASE 'store'

urlpatterns = [
    # 1. Django Administration Dashboard Route
    path('admin/', admin.site.urls),
    
    # 2. Customer Authentication Routes
    path('register/', store_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # 3. Include your app's URLs
    path('', include('store.urls')), # 👈 CHANGED TO LOWERCASE 'store'
]
# Add this code block at the absolute bottom of your main urls.py file
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
