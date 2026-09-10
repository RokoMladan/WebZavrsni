from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    nationality = models.CharField(max_length=100)
    birth_year = models.IntegerField()
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Artwork(models.Model):
    MEDIUM_CHOICES = [
        ('oil', 'Ulje na platnu'),
        ('watercolor', 'Akvarel'),
        ('digital', 'Digitalna umjetnost'),
        ('sculpture', 'Skulptura'),
        ('photography', 'Fotografija'),
    ]
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artworks')
    medium = models.CharField(max_length=20, choices=MEDIUM_CHOICES)
    year = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='artworks/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.artist.name}"

class Event(models.Model):
    EVENT_TYPE = [
        ('exhibition', 'Izložba'),
        ('workshop', 'Radionica'),
        ('lecture', 'Predavanje'),
        ('concert', 'Koncert'),
    ]
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE)
    description = models.TextField()
    location = models.CharField(max_length=300)
    date = models.DateField()
    start_time = models.TimeField()
    capacity = models.IntegerField()
    is_free = models.BooleanField(default=False)
    artworks = models.ManyToManyField(Artwork, blank=True, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FavoriteArtwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_artworks')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artwork')

    def __str__(self):
        return f"{self.user.username} → {self.artwork.title}"

class BookmarkedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"