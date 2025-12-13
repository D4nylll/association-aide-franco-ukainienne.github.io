from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, "Регистрация успешна!")
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})