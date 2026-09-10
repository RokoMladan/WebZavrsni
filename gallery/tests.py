from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Artist, Artwork, Event
import datetime

class ArtistModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            name="Testni Umjetnik",
            bio="Bio tekst",
            nationality="Hrvatska",
            birth_year=1980,
        )

    def test_artist_str(self):
        self.assertEqual(str(self.artist), "Testni Umjetnik")

    def test_artist_creation(self):
        self.assertEqual(Artist.objects.count(), 1)

class ArtworkModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Umjetnik", bio="x", nationality="HR", birth_year=1970)
        self.artwork = Artwork.objects.create(
            title="Slika",
            artist=self.artist,
            medium='oil',
            year=2020,
            description="Opis",
            price=500.00,
        )

    def test_artwork_str(self):
        self.assertIn("Slika", str(self.artwork))

    def test_artwork_relation(self):
        self.assertEqual(self.artwork.artist.name, "Umjetnik")

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='testpass123')
        self.artist = Artist.objects.create(name="A", bio="b", nationality="HR", birth_year=1990)

    def test_artwork_list_status(self):
        response = self.client.get(reverse('artwork-list'))
        self.assertEqual(response.status_code, 200)

    def test_artist_list_status(self):
        response = self.client.get(reverse('artist-list'))
        self.assertEqual(response.status_code, 200)

    def test_create_requires_login(self):
        response = self.client.get(reverse('artwork-create'))
        self.assertRedirects(response, '/login/?next=/artworks/new/')

    def test_login_and_create(self):
        self.client.login(username='test', password='testpass123')
        response = self.client.get(reverse('artwork-create'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'novi',
            'password1': 'Kompleksna123!',
            'password2': 'Kompleksna123!',
        })
        self.assertEqual(User.objects.filter(username='novi').count(), 1)

class SearchTest(TestCase):
    def setUp(self):
        artist = Artist.objects.create(name="Picasso", bio="x", nationality="ES", birth_year=1881)
        Artwork.objects.create(title="Guernica", artist=artist, medium='oil', year=1937, description="x")

    def test_search_by_title(self):
        response = self.client.get(reverse('htmx-search') + '?q=Guernica')
        self.assertContains(response, 'Guernica')

    def test_search_no_results(self):
        response = self.client.get(reverse('htmx-search') + '?q=zzznista')
        self.assertNotContains(response, 'Guernica')