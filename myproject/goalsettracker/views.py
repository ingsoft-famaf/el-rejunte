from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goalsettracker.forms import *
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from forms import UserCreationForm, AddGoalForm
from django.views.generic import CreateView
from django.views import generic

from .models import Goal

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
def index(request):
    return render(request, "index.html")

def goaldetail(request):
    return render(request, "goaldetail.html")

class Register(CreateView):
    """
    Vista de registro de usuario para uso de django. Posee la funcionalidad
    de crear nuevos usuarios con sus passwords. Hereda de
    django.views.generic.CreateView
    """
    template_name = 'registration/register.html'
    form_class = UserRegisterForm
    success_url = '/login/'

@login_required
def home(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
)

class AddGoal(CreateView):
    """
    Vista de registro de usuario para uso de django. Posee la funcionalidad
    de crear nuevos usuarios con sus passwords. Hereda de
    django.views.generic.CreateView
    """
    template_name = 'addgoal.html'
    form_class = AddGoalForm
    success_url = '/home/'

    