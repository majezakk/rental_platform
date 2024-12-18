from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Listing(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Название"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    address = models.CharField(
        max_length=200, verbose_name="Адрес"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="listings"
    )
    is_available = models.BooleanField(
        default=True, verbose_name="Доступно для аренды"
    )
    image1 = models.ImageField(
        upload_to='listings/images/',
        verbose_name="Изображение 1",
        blank=True, null=True
    )
    image2 = models.ImageField(
        upload_to='listings/images/',
        verbose_name="Изображение 2",
        blank=True, null=True
    )
    is_approved = models.BooleanField(
        default=False, verbose_name="Одобрено модератором"
    )

    def __str__(self):
        return self.title

# Сигналы для удаления изображений
@receiver(post_delete, sender=Listing)
def delete_images_with_listing(sender, instance, **kwargs):
    if instance.image1 and instance.image1.path:  # Проверяем, что файл существует
        if os.path.isfile(instance.image1.path):
            os.remove(instance.image1.path)
    if instance.image2 and instance.image2.path:
        if os.path.isfile(instance.image2.path):
            os.remove(instance.image2.path)


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = 'pending', _('В ожидании')
        APPROVED = 'approved', _('Подтверждено')
        DECLINED = 'declined', _('Отклонено')

    listing = models.ForeignKey(
        'Listing', on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Объявление"
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Арендатор"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(
        max_length=10, choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.listing.title} - {self.tenant.username} ({self.get_status_display()})"


class Review(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='reviews', verbose_name="Объявление")
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name="Арендатор")
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг", choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено модератором")

    def __str__(self):
        return f"{self.listing.title} - {self.tenant.username} ({self.rating}/5)"