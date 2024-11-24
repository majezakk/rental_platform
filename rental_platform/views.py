from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user})
    return render(request, 'home.html')

@login_required
def user_dashboard(request):
    if request.user.role == 'moderator':  # Если пользователь модератор
        return render(request, 'users/moderator_dashboard.html')
    elif request.user.role == 'landlord':  # Если пользователь арендодатель
        return render(request, 'users/landlord_dashboard.html')
    elif request.user.role == 'tenant':  # Если пользователь арендатор
        return render(request, 'users/tenant_dashboard.html')
    else:  # Если роль пользователя неизвестна
        return render(request, 'users/unknown_role.html')