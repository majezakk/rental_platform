from django.urls import path
from rental_platform.views import user_dashboard
from .views import register, user_login, user_logout


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
]
