from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from authentication.forms import  UserModelForm
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
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to create a new user
            return HttpResponse("User created successfully.")
    return render(request, 'authentication/register.html', {'form': form})
    




