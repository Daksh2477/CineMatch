from django.contrib import admin

from .models import Genre, Movie, UserRating


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'vote_average', 'popularity')
    list_filter = ('genres', 'release_year')
    search_fields = ('title', 'director')


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'updated_at')

# Register your models here.
