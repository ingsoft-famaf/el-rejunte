from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
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
    
    user = request.user
    print user
    
    all_goals = Goal.objects.order_by(order)
    user_goals = all_goals.filter(owner = user)
    
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
def addgoal(request, goal_id=None):

    if goal_id:
        goal = get_object_or_404(Goal, pk= goal_id)
        goal.last_modification = now()
        if goal.owner != request.user:
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response
    else:
        goal = Goal()
        goal.owner = request.user
        goal.state = 'inprogress'

    form = AddGoalForm(request.POST or None, instance = goal)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('/home')

    return render(request, 'goals/addgoal.html', {'form': form})

@login_required
def delete_goal(request, goal_id):

    goal = Goal.objects.get(pk = goal_id)
    if goal.owner != request.user:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    goal.delete()
    return HttpResponseRedirect('/home')

@login_required
def addsubgoal(request, goal_id):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddSubgoalForm(request.POST, goal_id)
        # check whether it's valid:
        if form.is_valid():
            goal= get_object_or_404(Goal, pk= goal_id)
            sub = form.save(commit=False)
            sub.maingoal = goal
            sub.state = False
            sub.save()
            return HttpResponseRedirect('/goal/'+ goal_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddSubgoalForm()

    return render(request, 'goals/addsubgoal.html', {'form': form})


def allgoaldetail(request):
    order = 'id'
    user = request.user
    print user
    all_goals = Goal.objects.order_by(order)
    user_goals = all_goals.filter(owner = user)
    subgoal_detail = Subgoal.objects.all()
    template = loader.get_template('goals/allgoaldetail.html')
    context = {
        'user_goals': user_goals,
        'subgoal_detail': subgoal_detail,
    }
    return HttpResponse(template.render(context, request))



def goaldetail(request, goal_id):
    goal_detail = get_object_or_404(Goal, pk= goal_id)
    if goal_detail.owner != request.user:
        response = HttpResponse("You do not have permission to view this.")
        response.status_code = 403
        return response
    else:
        all_subgoal= Subgoal.objects.all()
        subgoal_detail = all_subgoal.filter(maingoal = goal_detail)
        template = loader.get_template('goals/goaldetail.html')
        context = {
            'goal_detail': goal_detail,
            'subgoal_detail': subgoal_detail,
         }
        return HttpResponse(template.render(context, request))

def subgoalupdate(subgoal_id):
    subgoal = get_object_or_404(Subgoal, pk= goal_id)
    subgoal.state = True
    subgoal.save


@login_required
def newcategory(request):
    """
    Vista de agregar meta.
    Crea nuevas metas.
    """
    pk = request.user.id
    user = User.objects.get(pk=pk)


@login_required
def NewCategory(request):
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewCategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user_id = request.user.id
            user = get_object_or_404(User, pk= user_id)
            category = form.save(commit=False)
            category.owner = user
            category.save()
            return HttpResponseRedirect('/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewCategoryForm()

    return render(request, 'categoria/nuevacategoria.html', {'form': form})









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

@login_required
def miscategorias(request):
    user = request.user
    catlist = Categoria.objects.filter(owner=user)
    if catlist:
        if catlist[0].owner != user:
            response = HttpResponse("You do not have permission to view this.")
            response.status_code = 403
            return response            
    template = loader.get_template('categoria/showcats.html')
    context = {'catlist': catlist,}
    return HttpResponse(template.render(context, request))
