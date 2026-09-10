from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    # Artists
    path('artists/', views.ArtistListView.as_view(), name='artist-list'),
    path('artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    path('artists/new/', views.ArtistCreateView.as_view(), name='artist-create'),
    path('artists/<int:pk>/edit/', views.ArtistUpdateView.as_view(), name='artist-update'),
    path('artists/<int:pk>/delete/', views.ArtistDeleteView.as_view(), name='artist-delete'),

    # Artworks
    path('artworks/', views.ArtworkListView.as_view(), name='artwork-list'),
    path('artworks/<int:pk>/', views.ArtworkDetailView.as_view(), name='artwork-detail'),
    path('artworks/new/', views.ArtworkCreateView.as_view(), name='artwork-create'),
    path('artworks/<int:pk>/edit/', views.ArtworkUpdateView.as_view(), name='artwork-update'),
    path('artworks/<int:pk>/delete/', views.ArtworkDeleteView.as_view(), name='artwork-delete'),
    path('artworks/<int:pk>/favorite/', views.toggle_favorite, name='toggle-favorite'),

    # Events
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('events/new/', views.EventCreateView.as_view(), name='event-create'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('events/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle-bookmark'),

    # Kolekcija
    path('moja-kolekcija/', views.my_collection, name='my-collection'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # HTMX
    path('htmx/search/', views.artwork_search_htmx, name='htmx-search'),
]