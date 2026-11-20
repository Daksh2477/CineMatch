from django.contrib import admin

from .models import RecommendationHistory


@admin.register(RecommendationHistory)
class RecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'source_movie', 'mode', 'created_at')

# Register your models here.
