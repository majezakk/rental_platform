from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

User = get_user_model()

# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Вход
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Неверные данные'})
    return render(request, 'users/login.html')

# Выход
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def manage_users(request):
    if request.user.role != 'moderator':
        return redirect('home')

    users = User.objects.exclude(id=request.user.id).order_by('role', 'username')  # Исключаем самого модератора
    return render(request, 'users/manage_users.html', {'users': users})

@login_required
def update_user_role(request, pk, role):
    if request.user.role != 'moderator':
        return redirect('home')

    user = get_object_or_404(User, pk=pk)
    user.role = role
    user.save()
    messages.success(request, f"Роль пользователя {user.username} обновлена на {role}.")
    return redirect('manage_users')

@login_required
def delete_user(request, pk):
    if request.user.role != 'moderator':
        return redirect('home')

    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, f"Пользователь {user.username} удален.")
    return redirect('manage_users')