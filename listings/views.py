from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm

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
