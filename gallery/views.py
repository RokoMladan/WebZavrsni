from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Artist, Artwork, Event, FavoriteArtwork, BookmarkedEvent
from .forms import ArtworkForm, ArtistForm, EventForm

# Mixin koji dopušta pristup samo adminu
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
    
    def handle_no_permission(self):
        raise PermissionDenied

# --- ARTIST ---
class ArtistListView(ListView):
    model = Artist
    template_name = 'gallery/artist_list.html'
    context_object_name = 'artists'

    def get_queryset(self):
        qs = super().get_queryset().order_by('name')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(nationality__icontains=q))
        return qs

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'gallery/artist_detail.html'

class ArtistCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'gallery/form.html'
    success_url = reverse_lazy('artist-list')

class ArtistUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'gallery/form.html'
    success_url = reverse_lazy('artist-list')

class ArtistDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Artist
    template_name = 'gallery/confirm_delete.html'
    success_url = reverse_lazy('artist-list')

# --- ARTWORK ---
class ArtworkListView(ListView):
    model = Artwork
    template_name = 'gallery/artwork_list.html'
    context_object_name = 'artworks'

    def get_queryset(self):
        qs = super().get_queryset().select_related('artist').order_by('-year')
        q = self.request.GET.get('q')
        medium = self.request.GET.get('medium')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(artist__name__icontains=q))
        if medium:
            qs = qs.filter(medium=medium)
        return qs

class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'gallery/artwork_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['is_favorite'] = FavoriteArtwork.objects.filter(
                user=self.request.user, artwork=self.object
            ).exists()
        return ctx

class ArtworkCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'gallery/form.html'
    success_url = reverse_lazy('artwork-list')

class ArtworkUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'gallery/form.html'
    success_url = reverse_lazy('artwork-list')

class ArtworkDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Artwork
    template_name = 'gallery/confirm_delete.html'
    success_url = reverse_lazy('artwork-list')

# --- EVENT ---
class EventListView(ListView):
    model = Event
    template_name = 'gallery/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        qs = super().get_queryset().order_by('date')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(location__icontains=q))
        return qs

class EventDetailView(DetailView):
    model = Event
    template_name = 'gallery/event_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['is_bookmarked'] = BookmarkedEvent.objects.filter(
                user=self.request.user, event=self.object
            ).exists()
        return ctx

class EventCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'gallery/form.html'
    success_url = reverse_lazy('event-list')

class EventUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'gallery/form.html'
    success_url = reverse_lazy('event-list')

class EventDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Event
    template_name = 'gallery/confirm_delete.html'
    success_url = reverse_lazy('event-list')

# --- FAVORITI I BOOKMARKI ---
@login_required
def toggle_favorite(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    fav, created = FavoriteArtwork.objects.get_or_create(user=request.user, artwork=artwork)
    if not created:
        fav.delete()
    return redirect('artwork-detail', pk=pk)

@login_required
def toggle_bookmark(request, pk):
    event = get_object_or_404(Event, pk=pk)
    bm, created = BookmarkedEvent.objects.get_or_create(user=request.user, event=event)
    if not created:
        bm.delete()
    return redirect('event-detail', pk=pk)

@login_required
def my_collection(request):
    favorites = FavoriteArtwork.objects.filter(user=request.user).select_related('artwork__artist')
    bookmarks = BookmarkedEvent.objects.filter(user=request.user).select_related('event')
    return render(request, 'gallery/my_collection.html', {
        'favorites': favorites,
        'bookmarks': bookmarks,
    })

# --- AUTH ---
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'gallery/register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'gallery/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'gallery/home.html', {
        'recent_artworks': Artwork.objects.order_by('-created_at')[:6],
        'upcoming_events': Event.objects.order_by('date')[:3],
    })

# HTMX live search
def artwork_search_htmx(request):
    q = request.GET.get('q', '')
    artworks = Artwork.objects.filter(
        Q(title__icontains=q) | Q(artist__name__icontains=q)
    ).select_related('artist')[:10]
    return render(request, 'gallery/partials/artwork_results.html', {'artworks': artworks})