"""Views for the Users app"""
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    """Load the account registration page"""
    if request.method != 'POST':
        # If this isn't a POST request, load a default blank user creation form
        form = UserCreationForm()
    else:
        # If this is POST, process the form.
        #  Check if it's valid, and if so, save the user to the DB, and
        #  redirect to the home page.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('commons:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)
