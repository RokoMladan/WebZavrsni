from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Artist, Artwork, Event

class CustomClearableFileInput(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = ''
        if value and hasattr(value, 'url'):
            html += format_html(
                '<div class="flex items-center gap-2 text-stone-400 text-sm mb-2">'
                'Currently: <a href="{}" class="text-amber-400 hover:underline truncate max-w-xs">{}</a>'
                '</div>',
                value.url, value
            )
            html += format_html(
                '<div class="flex items-center gap-2 text-stone-400 text-sm mb-2">'
                '<label for="{}-clear_id" class="cursor-pointer hover:text-amber-400">Clear</label>'
                '<input type="checkbox" name="{}-clear" id="{}-clear_id" class="w-4 h-4 accent-amber-400 cursor-pointer">'
                '</div>',
                name, name, name
            )
            html += '<div class="text-stone-400 text-sm mb-1">Change:</div>'
        
        file_input = super(forms.ClearableFileInput, self).render(name, None, attrs, renderer)
        html += file_input
        return mark_safe(html)

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'bio', 'nationality', 'birth_year', 'website', 'image']
        widgets = {
            'image': CustomClearableFileInput(),
        }

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'artist', 'medium', 'year', 'description', 'image', 'price', 'is_available']
        widgets = {
            'image': CustomClearableFileInput(),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'description', 'location', 'date', 'start_time', 'capacity', 'is_free', 'artworks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'artworks': forms.SelectMultiple(attrs={'size': '8'}),
        }