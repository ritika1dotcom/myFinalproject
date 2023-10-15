from django.shortcuts import render
from .form import GenreSelectForm

def select_genres(request):
    if request.method == "POST":
        form = GenreSelectForm(request.POST)
        if form.is_valid():
            genres_selected = form.cleaned_data['genres']
            # Do something with the selected genres
    else:
        form = GenreSelectForm()

    return render(request, 'select_genres.html', {'form': form})

# Create your views here.
def show_base(request):
    return render(request, 'home.html')
def album_view(request):
    return render(request, 'album.html')
def collections_view(request):
    return render(request, 'collections.html')
# views.py

