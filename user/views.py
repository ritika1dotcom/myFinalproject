from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail

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
    return render(request, 'base.html', {'form': form})

def send_welcome_email(recipient_email):
    send_mail(
        'Welcome to Our Site',
        'Thank you for registering with us. We hope you enjoy our services.',
        'webmaster@example.com',  # This should be your sending email
        [recipient_email],
        fail_silently=False,  # This will raise an exception if there's an issue
    )
