from django.shortcuts import render

# Create your views here.
def show_base(request):
    return render(request, 'home.html')
def album_view(request):
    return render(request, 'album.html')
def collections_view(request):
    return render(request, 'collections.html')

