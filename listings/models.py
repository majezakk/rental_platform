from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = 'pending', _('В ожидании')
        APPROVED = 'approved', _('Подтверждено')
        DECLINED = 'declined', _('Отклонено')

    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bookings', verbose_name="Объявление")
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name="Арендатор")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(max_length=10, choices=BookingStatus.choices, default=BookingStatus.PENDING, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.listing.title} - {self.tenant.username} ({self.get_status_display()})"