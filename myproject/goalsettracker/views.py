from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.shortcuts import get_object_or_404, render
=======
from django.http import HttpResponse
from django.shortcuts import render
>>>>>>> 1ed100d5e198bbee02c706a25bddf763f37b6898
from django.shortcuts import render_to_response
from django.template import loader
from django.views.generic import CreateView

from .forms import *
from .models import Goal, Subgoal, Categoria


# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
def index(request):
    return render(request, "index.html")


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
    order = 'id'

    user = currentuser(request)
    print user
<<<<<<< HEAD
    
    all_goals = Goal.objects.order_by(order)
    user_goals = all_goals.filter(owner = user)
    
=======
    user_goals = Goal.objects.order_by(order)

>>>>>>> 1ed100d5e198bbee02c706a25bddf763f37b6898
    template = loader.get_template('home.html')
    context = {
        'user': request.user,
        'user_goals': user_goals,
    }
    return HttpResponse(template.render(context, request))


@login_required
def deactivate_user(request):
    # IMPORTANT!
    # is_active:
    # Boolean.Designates whether this user account should be considered active.We recommend that you set this flag to
    # False instead of deleting accounts; that way,if your applications have any foreign keys to users, the foreign keys
    # won't break.
    # This doesn't necessarily control whether or not the user can log in. Authentication backends aren't required to
    # check for the is_active flag but the default backend (ModelBackend) and the RemoteUserBackend do. You can use
    # AllowAllUsersModelBackend or AllowAllUsersRemoteUserBackend if you want to allow inactive users to login. In this
    # case, you'll also want to customize the AuthenticationForm used by the login() view as it rejects inactive users.
    # Be aware that the permission-checking methods such as has_perm() and the authentication in the Django admin all
    # return False for inactive users.
    # https://docs.djangoproject.com/es/1.10/ref/contrib/auth/#django.contrib.auth.models.User.is_active
    pk = request.user.id
    user = User.objects.get(pk=pk)
    if request.user.is_authenticated() and request.user.id == user.id:
        # if request.method == "POST":
        user_form = DeactivateUserForm(request.POST, instance=user)
        if user_form.is_valid():
            user.is_active = False
            user.save()
            # es necesario mandar un mail?
            # email_user(subject, message, from_email=None, **kwargs)
        return render(request, "deactivate_user.html", {"user_form": user_form, })


@login_required
def addgoal(request):
    """
    Vista de agregar meta. 
    Crea nuevas metas. 
    """
    pk = request.user.id
    user = User.objects.get(pk=pk)


class AddGoal(CreateView):
    """
    Vista de registro de usuario para uso de django. Posee la funcionalidad
    de crear nuevos usuarios con sus passwords. Hereda de
    django.views.generic.CreateView
    """
    template_name = 'goals/addgoal.html'
    form_class = AddGoalForm
    success_url = '/home'


def currentuser(request):
    user = request.user
    return user

"""
def allgoaldetail(request):
    filtro = 1
    goal_detail = Goal.objects.filter(pk=filtro)[:1]
    subgoal_detail = Subgoal.objects.all()
    template = loader.get_template('goals/goaldetail.html')
    context = {
        'goal_detail': goal_detail,
        'subgoal_detail': subgoal_detail,
    }
    return HttpResponse(template.render(context, request))
<<<<<<< HEAD
"""


def goaldetail(request, goal_id):
    goal_detail = get_object_or_404(Goal, pk= goal_id)
    #goal_detail = Goal.objects.filter(pk = goal_id)[:1]
    all_subgoal= Subgoal.objects.all()
    subgoal_detail = all_subgoal.filter(maingoal = goal_detail)
    template = loader.get_template('goals/goaldetail.html')
    context = {
        'goal_detail': goal_detail,
        'subgoal_detail': subgoal_detail,
    }
    return HttpResponse(template.render(context, request))


=======


@login_required
def newcategory(request):
    """
    Vista de agregar meta.
    Crea nuevas metas.
    """
    pk = request.user.id
    user = User.objects.get(pk=pk)


class NewCategory(CreateView):
    template_name = 'categoria/nuevacategoria.html'
    form_class = NewCategoryForm
    success_url = '/home'


# def new_category(request):
#
#     if request.method == 'POST':
#         form = NewCategoryForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             request.user.message_set.create(message="Categoria creada con exito")
#             return HttpResponse('/home')
#     else:
#         form = NewCategoryForm("","",request.user)
#     return render(request, 'categoria/nuevacategoria.html', {'form': form, 'owner': request.user})


def miscategorias(request):
    user = request.user
    catlist = Categoria.objects.filter(owner=user)
    template = loader.get_template('categoria/showcats.html')
    context = {'catlist': catlist,}
    return HttpResponse(template.render(context, request))
>>>>>>> 1ed100d5e198bbee02c706a25bddf763f37b6898
