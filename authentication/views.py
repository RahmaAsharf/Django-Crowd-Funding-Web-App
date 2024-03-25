from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from authentication.forms import  UserModelForm, UserProfileForm, CustomUser


# Create your views here.
def landing(request):
    
    return render(request,"authentication/landing.html")
# def profile(request):
#     url = reverse('index')
#     return redirect(url)
#     # return HttpResponse("Login successfully ")


def register(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to create a new user
            return HttpResponse("User created successfully.")
    return render(request, 'authentication/register.html', {'form': form})
    

def view_profile(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    return render(request, 'authentication/profile.html', {'user': user})


def edit_profile(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view.profile', id=id)
    else:
        # form = UserModelForm(instance=user)
        # Set initial password field to empty string when editing profile
        form = UserProfileForm(instance=user, initial={'password': ''}) 
    return render(request, 'authentication/edit_profile.html', {'form': form, 'id': id})


def delete_account(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    if request.method == 'POST':
        user.delete()
        return redirect('landing') 
    return render(request, 'authentication/delete_account.html', {'user': user})
