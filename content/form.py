from django import forms

class GenreSelectForm(forms.Form):
    GENRE_CHOICES = [
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
        ('pop', 'Pop'),
        # ... add as many genres as you like
    ]
    genres = forms.MultipleChoiceField(
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select text-black bg-white',
            'size': len(GENRE_CHOICES)
        }),
        choices=GENRE_CHOICES
    )
