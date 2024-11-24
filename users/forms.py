from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Определяем новые варианты ролей для формы
ROLE_CHOICES = [
    ('landlord', 'Арендодатель'),
    ('tenant', 'Арендатор'),
]

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Роль')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')