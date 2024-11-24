from django.db import models
from django.conf import settings

class Listing(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="listings"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступно для аренды")
    image1 = models.ImageField(upload_to='listings/images/', verbose_name="Изображение 1", blank=True, null=True)
    image2 = models.ImageField(upload_to='listings/images/', verbose_name="Изображение 2", blank=True, null=True)

    def __str__(self):
        return self.title
