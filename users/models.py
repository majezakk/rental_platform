from django.contrib.auth.models import AbstractUser
from django.db import models

# Роли пользователей
USER_ROLES = [
    ('moderator', 'Модератор'),
    ('landlord', 'Арендодатель'),
    ('tenant', 'Арендатор'),
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLES, default='tenant')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
