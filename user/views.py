import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .form import AvatarForm
from .models import PlayHistory, UserProfile
from django.http import JsonResponse

def password_reset_done_with_message(request):
    messages.success(request, 'Password reset email has been sent!')
    return render(request, 'password_reset_done_with_message.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'There was an error creating your account.')
    else:
        form = UserCreationForm()
    return render(request, 'home.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error creating your account.')
    else:
        form = AvatarForm()
    return render(request, 'home.html', {'form': form})


def send_welcome_email(recipient_email):
    send_mail(
        'Welcome to Our Site',
        'Thank you for registering with us. We hope you enjoy our services.',
        'webmaster@example.com',  # This should be your sending email
        [recipient_email],
        fail_silently=False,  # This will raise an exception if there's an issue
    )

def user_song_history(request, username):
    user_obj = get_object_or_404(User, username=username)
    song_history = PlayHistory.objects.filter(user=user_obj).order_by('-date_played')  # newest songs first
    context = {
        'user_obj': user_obj,
        'song_history': song_history
    }
    return render(request, 'song_history.html', context)

def add_song_history(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        song_title = data.get('song_title')
        artist_name = data.get('artist_name')
    
        if not song_title or not artist_name:
            return JsonResponse({'status': 'error', 'message': 'Missing song details'}, status=400)
        
        PlayHistory.objects.create(
            user=request.user,
            song_title=song_title,
            artist_name=artist_name
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok', 'message': 'valid request'})

def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.avatar = form.cleaned_data['avatar']
            user_profile.save()
            return redirect('profile')
    else:
        form = AvatarForm()
    return render(request, 'song_history.html', {'form': form})