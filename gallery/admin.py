from django.contrib import admin
from .models import Artist, Artwork, Event, FavoriteArtwork, BookmarkedEvent

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_year']
    search_fields = ['name', 'nationality']

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'medium', 'year', 'is_available', 'price']
    search_fields = ['title', 'artist__name']
    list_filter = ['medium', 'is_available']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'is_free', 'capacity']
    search_fields = ['title', 'location']
    list_filter = ['event_type', 'is_free']

@admin.register(FavoriteArtwork)
class FavoriteArtworkAdmin(admin.ModelAdmin):
    list_display = ['user', 'artwork', 'created_at']

@admin.register(BookmarkedEvent)
class BookmarkedEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'created_at']