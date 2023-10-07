from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def password_reset_done_with_message(request):
    messages.success(request, 'Password reset email has been sent!')
    return redirect('password_reset_done')

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
