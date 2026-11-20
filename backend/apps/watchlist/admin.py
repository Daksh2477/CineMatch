from django.contrib import admin

from .models import WatchlistItem


@admin.register(WatchlistItem)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')

# Register your models here.
