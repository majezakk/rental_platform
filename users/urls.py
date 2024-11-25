from django.urls import path
from rental_platform.views import user_dashboard
from . import views
from .views import register, user_login, user_logout, edit_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),

    path('manage/', views.manage_users, name='manage_users'),
    path('update-role/<int:pk>/<str:role>/', views.update_user_role, name='update_user_role'),
    path('delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('edit/', edit_profile, name='edit_profile'),

]
