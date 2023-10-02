from django.shortcuts import render

# Create your views here.
def show_base(request):
    return render(request, 'base.html')

