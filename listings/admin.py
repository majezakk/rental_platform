from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'owner', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at', 'owner')
    search_fields = ('title', 'address', 'owner__username')
