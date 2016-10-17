from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
def index(request):
    return render(request, "index.html")

def meta(request):
    return render(request, "meta.html")

@login_required(login_url="login/")
def home(request):
    return render(request, "home.html")
