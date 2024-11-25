from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing, Booking, Review
from .forms import ListingForm, BookingForm, ReviewForm
from django.contrib import messages
from datetime import date


def listing_list(request):
    listings = Listing.objects.filter(is_approved=True, is_available=True)
    return render(request, 'listings/listing_list.html', {'listings': listings})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    # Фильтруем только одобренные отзывы
    approved_reviews = listing.reviews.filter(is_approved=True)

    # Проверяем доступность объявления для арендаторов
    if not listing.is_approved and request.user.role == 'tenant':
        return redirect('listing_list')  # Перенаправляем на список доступных объявлений

    return render(request, 'listings/listing_detail.html', {'listing': listing, 'reviews': approved_reviews})


@login_required
def listing_create(request):
    if request.user.role != 'landlord':
        return redirect('home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('listing_list')
    else:
        form = ListingForm()
    return render(request, 'listings/listing_form.html', {'form': form})

@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {'form': form})

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('listing_list')
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})


@login_required
def create_booking(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user.role != 'tenant':
        return redirect('home')

    # Проверка на существующее активное бронирование
    existing_booking = Booking.objects.filter(
        listing=listing,
        tenant=request.user,
        status=Booking.BookingStatus.APPROVED,
        end_date__gte=date.today()  # Только активные бронирования
    ).exists()

    if existing_booking:
        messages.error(request, "У вас уже есть активное бронирование для этого объекта.")
        return redirect('listing_detail', pk=listing.pk)

    # Обработка формы
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.tenant = request.user
            booking.save()
            messages.success(request, "Ваше бронирование отправлено на рассмотрение.")
            return redirect('booking_list_tenant')
    else:
        form = BookingForm()

    return render(request, 'listings/create_booking.html', {'form': form, 'listing': listing})

@login_required
def booking_list_tenant(request):
    if request.user.role != 'tenant':
        return redirect('home')

    bookings = request.user.bookings.all()
    return render(request, 'listings/booking_list_tenant.html', {'bookings': bookings})

@login_required
def booking_list_landlord(request):
    if request.user.role != 'landlord':
        return redirect('home')

    listings = request.user.listings.all()
    bookings = Booking.objects.filter(listing__in=listings).order_by('-created_at')
    return render(request, 'listings/booking_list_landlord.html', {'bookings': bookings})

@login_required
def booking_list_landlord(request):
    if request.user.role != 'landlord':
        return redirect('home')

    listings = request.user.listings.all()
    bookings = Booking.objects.filter(listing__in=listings).order_by('-created_at')
    return render(request, 'listings/booking_list_landlord.html', {'bookings': bookings})


@login_required
def manage_booking(request, pk, action):
    # Проверяем, что пользователь является владельцем объявления
    booking = get_object_or_404(Booking, pk=pk, listing__owner=request.user)

    if action == 'approve':
        booking.status = Booking.BookingStatus.APPROVED
    elif action == 'decline':
        booking.status = Booking.BookingStatus.DECLINED
    else:
        # Если действие не распознано, перенаправляем назад
        return redirect('booking_list_landlord')

    booking.save()  # Сохраняем изменения
    return redirect('booking_list_landlord')  # Возвращаемся к списку бронирований


@login_required
def create_review(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user.role != 'tenant':
        return redirect('home')

    # Проверка, оставлял ли арендатор уже отзыв для этого объявления
    existing_review = Review.objects.filter(listing=listing, tenant=request.user).exists()
    if existing_review:
        messages.error(request, "Вы уже оставили отзыв для этого объявления.")
        return redirect('listing_detail', pk=listing.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.tenant = request.user
            review.save()
            messages.success(request, "Ваш отзыв отправлен на модерацию.")
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ReviewForm()

    return render(request, 'listings/create_review.html', {'form': form, 'listing': listing})

@login_required
def moderate_reviews(request):
    if request.user.role != 'moderator':
        return redirect('home')

    reviews = Review.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'listings/moderate_reviews.html', {'reviews': reviews})

@login_required
def manage_review(request, pk, action):
    if request.user.role != 'moderator':
        return redirect('home')

    review = get_object_or_404(Review, pk=pk)
    if action == 'approve':
        review.is_approved = True
        review.save()
        messages.success(request, "Отзыв одобрен.")
    elif action == 'delete':
        review.delete()
        messages.success(request, "Отзыв удален.")

    return redirect('moderate_reviews')


@login_required
def moderate_listings(request):
    if request.user.role != 'moderator':
        return redirect('home')

    listings = Listing.objects.filter(is_approved=False)
    return render(request, 'listings/moderate_listings.html', {'listings': listings})

@login_required
def manage_listing(request, pk, action):
    if request.user.role != 'moderator':
        return redirect('home')

    listing = get_object_or_404(Listing, pk=pk)

    if action == 'approve':
        listing.is_approved = True
        listing.save()
        messages.success(request, f"Объявление '{listing.title}' одобрено.")
    elif action == 'decline':
        listing.delete()
        messages.success(request, f"Объявление '{listing.title}' отклонено и удалено.")

    return redirect('moderate_listings')