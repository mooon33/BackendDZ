
from django.urls import path, include

from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import custom_logout
from .forms import CustomLoginForm


from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ProductListView,
    ProductDetailView,
    register,
    ProfileView,
    home  # Добавляем home view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html',authentication_form=CustomLoginForm), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')), 
    path('', views.home, name='home'),
]