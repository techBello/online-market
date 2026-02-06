from django.shortcuts import render, redirect # type: ignore

# Create your views here.
def home(request):
    return render(request, 'home.html')