from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing, Booking
from .forms import ListingForm, BookingForm


def listing_list(request):
    listings = Listing.objects.filter(is_available=True)
    return render(request, 'listings/listing_list.html', {'listings': listings})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})


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

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.tenant = request.user
            booking.save()
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