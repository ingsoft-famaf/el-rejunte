from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views.generic import CreateView

from .forms import *
from .models import Goal, Subgoal, Categoria, Comment


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


def failmail(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    subject = 'GST - El tiempo de la meta ha expirado.'
    message = 'La meta ' + goal.name + ' ha expirado. Ponete las pilas'
    to = [goal.owner.email]
    EmailMessage(subject, message, to=to).send()


@login_required
def home(request, order_by='id'):
    user = request.user
    all_goals = Goal.objects.order_by(str(order_by))
    user_goals = all_goals.filter(owner=user)
    for ug in user_goals:
            goalupdate(request, ug.id)
    template = loader.get_template('home.html')
    context = {
        'user': request.user,
        'user_goals': user_goals,
        'selected': order_by,
    }
    return HttpResponse(template.render(context, request))


@login_required
def deactivate_user(request):
    pk = request.user.id
    user = User.objects.get(pk=pk)
    form = DeactivateUserForm(request.POST or None, instance=user)
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            if form.is_valid():
                if form.clean_is_active():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    return HttpResponseRedirect(reverse_lazy('logout'))
                else:
                    return HttpResponseRedirect('/home')
        return render(request, "deactivate_user.html", {"form": form})
    else:
        return HttpResponseRedirect("/home")


@login_required
def addgoal(request, goal_id=None):
    if goal_id:
        goal = get_object_or_404(Goal, pk=goal_id)
        goal.last_modification = now()
        if goal.owner != request.user:
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response
    else:
        goal = Goal()
        goal.owner = request.user
        goal.state = 'inprogress'

    form = AddGoalForm(request.POST or None, request.FILES or None, instance=goal)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('/home')

    return render(request, 'goals/addgoal.html', {'form': form})

@login_required
def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('/profile')

    return render(request, 'edit_profile.html', {'form': form})



@login_required
def add_profile_photo(request, myuser_id=None):
    if myuser_id:
        myuser = get_object_or_404(MyUser, pk=myuser_id)
        if myuser.owner != request.user:
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response
    else:
        myuser = MyUser()
        myuser.owner = request.user
    form = MyUserForm(request.POST or None, request.FILES or None, instance=myuser)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('/profile')
    return render(request, 'addphoto.html', {'form': form})


@login_required
def delete_confirm_photo(request, myuser_id):
    myuser = get_object_or_404(MyUser, pk=myuser_id)
    if myuser.owner != request.user:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    if request.method == "POST":
        myuser.delete()
        return HttpResponseRedirect('/profile')
    context = {
        "myuser": myuser,
    }
    return render(request, "delete_confirm_photo.html", context)





@login_required
def goaldetail(request, goal_id):
    goalupdate(request, goal_id)
    progress_bar = progressbar(request, goal_id)
    goal_detail = get_object_or_404(Goal, pk=goal_id)
    if goal_detail.owner != request.user:
        response = HttpResponse("You do not have permission to view this.")
        response.status_code = 403
        return response
    else:

        comment_form = AddCommentForm(request.POST or None)
        if comment_form.is_valid() and request.method == 'POST':
            content_data=comment_form.cleaned_data.get("content")
            new_comment = Comment.objects.get_or_create(
                            maingoal = goal_detail,
                            content = content_data
                        )


        subgoal_detail = Subgoal.objects.filter(maingoal=goal_detail)
        comments_detail = Comment.objects.filter(maingoal=goal_detail).order_by('-timestamp')
        template = loader.get_template('goals/goaldetail.html')
        context = {
            'goal_detail': goal_detail,
            'subgoal_detail': subgoal_detail,
            'comments_detail': comments_detail,
            'comment_form':comment_form,
            'progress_bar':progress_bar,
        }
        return HttpResponse(template.render(context, request))

    
@login_required
def goalfilter(request):
    user = request.user
    if request.method == 'GET':
        # catList = Categoria.objects.filter(owner=user)
        form = GoalFilterForm(owner=user)
        user_goals = Goal.objects.filter(owner=user)
        context = {'form': form, 'user_goals': user_goals}
        response = render(request, 'goals/goalfilter.html', context)
    elif request.method == 'POST':
        form = GoalFilterForm(user, request.POST)
        if form.is_valid():
            user_goals = Goal.objects.filter(owner=user)
            # nombre estado fechainicio fechafin categoria
            item = form.cleaned_data['nombre']
            if item:
                user_goals = user_goals.filter(name=item)

            item = form.cleaned_data['estado']
            if item:
                user_goals = user_goals.filter(state=item)

            item = form.cleaned_data['fechainicio']
            if item:
                user_goals = user_goals.filter(creationdate__gte=item)

            item = form.cleaned_data['fechafin']
            if item:
                user_goals = user_goals.filter(finishdate__lte=item)

            item = form.cleaned_data['categoria']
            if item:
                user_goals = user_goals.filter(category=item)

            context = {'form': form, 'user_goals': user_goals}
            response = render(request, 'goals/goalfilter.html', context)
        else:
            response = HttpResponse("Formulario invalido2")
    return response


@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    if goal.owner != request.user:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    if request.method == "POST":
        goal.delete()
        return HttpResponseRedirect('/home')
    context = {
        "goal": goal
    }

    return render(request, "goals/delete_confirm_goal.html", context)


@login_required
def delete_confirm_comment(request, goal_id, comment_id):
    goal = get_object_or_404(Goal,pk=goal_id)
    if goal.owner != request.user:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    comment = get_object_or_404(Comment,pk=comment_id)
    if request.method == "POST":
        comment.delete()
        return HttpResponseRedirect('/goal/' + goal_id)
    context = {
        "comment": comment,
        "goal": goal
    }
    return render(request, "goals/delete_confirm_comment.html", context)


@login_required
def delete_category(request, category_id):
    category = Categoria.objects.get(pk=category_id)
    if category.owner != request.user:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
    else:
        user = User.objects.get(pk=request.user.id)
        goals_in_cat = Goal.objects.filter(owner=user, category=category.id)
        try:
            uncategorized = Categoria.objects.get(name="Uncategorized")
        except:
            uncategorized = Categoria.objects.create(name="Uncategorized", owner=user, )
        for goal in goals_in_cat:
            goal.category = uncategorized
            goal.save()
        if category != uncategorized:
            category.delete()
        response = HttpResponseRedirect('/miscategorias')
    return response


@login_required
def addsubgoal(request, goal_id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddSubgoalForm(request.POST, goal_id)
        # check whether it's valid:
        if form.is_valid():
            goal = get_object_or_404(Goal, pk=goal_id)
            sub = form.save(commit=False)
            sub.maingoal = goal
            sub.state = False
            sub.save()
            return HttpResponseRedirect('/goal/' + goal_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddSubgoalForm()

    return render(request, 'goals/addsubgoal.html', {'form': form})


@login_required
def allgoaldetail(request):
    order = 'id'
    user = request.user
    all_goals = Goal.objects.order_by(order)
    user_goals = all_goals.filter(owner=user)
    subgoal_detail = Subgoal.objects.all()
    template = loader.get_template('goals/allgoaldetail.html')
    context = {
        'user_goals': user_goals,
        'subgoal_detail': subgoal_detail,
    }
    return HttpResponse(template.render(context, request))


@login_required
def goalupdate(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    all_subgoal = Subgoal.objects.all()
    subgoals = all_subgoal.filter(maingoal=goal)
    cant = subgoals.count()
    if cant == 0:
        complete = False
    if cant > 0:
        complete = True
    
    if goal.state == 'done' and cant == 0:
        print cant
        return

    if goal.state == 'inprogress' and goal.finishdate < now():
        goal.state = 'fail'
        goal.save()
        failmail(request, goal_id)

    if goal.state == 'inprogress' or goal.state == 'done':
        for subs in subgoals:
            if subs.state == False:
                complete = False
        if complete == True:
            goal.state = 'done'
            goal.save()

        if complete == False:
            goal.state = 'inprogress'
            goal.save()


@login_required
def allgoalupdate():
    all_goals = Subgoal.objects.all()
    for goals in all_goals:
        goalupdate(goals.id)


@login_required
def addmoretime(request, goal_id):
    return HttpResponseRedirect('/home')


@login_required
def completesubgoal(request, goal_id, subgoal_id):
    subgoal = get_object_or_404(Subgoal, pk=subgoal_id)
    subgoal.state = True
    subgoal.save()
    return HttpResponseRedirect('/goal/' + goal_id)


@login_required
def deletesubgoal(request, goal_id, subgoal_id):
    subgoal = get_object_or_404(Subgoal, pk=subgoal_id)
    subgoal.delete()
    return HttpResponseRedirect('/goal/' + goal_id)


@login_required
def subgoalupdate(subgoal_id):
    subgoal = get_object_or_404(Subgoal, pk=subgoal_id)
    subgoal.state = True
    subgoal.save()

@login_required
def completegoal(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    all_subgoal = Subgoal.objects.all()
    subgoals = all_subgoal.filter(maingoal=goal)
    goal.state = 'done'
    goal.save()
    print goal.state
    for subs in subgoals:
        subs.state = True
        subs.save()

    return HttpResponseRedirect('/goal/' + goal_id)


@login_required
def newcategory(request):
    """
    Vista de agregar meta.
    Crea nuevas metas.
    """
    pk = request.user.id
    user = User.objects.get(pk=pk)


@login_required
def new_category(request, category_id=None):
    if category_id:
        category = get_object_or_404(Categoria, pk=category_id)
        category.last_modification = now()
        if category.owner != request.user:
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response
    else:
        category = Categoria()
        category.owner = request.user

    form = NewCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('/miscategorias')
    return render(request, 'categoria/nuevacategoria.html', {'form': form})

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
    context = {'catlist': catlist, }
    return HttpResponse(template.render(context, request))

@login_required
def profile(request):
    user = request.user
    myuser = MyUser.objects.filter(owner=user)
    if myuser:
        myuser = myuser[0]
    context = {'user':user,
               'myuser': myuser,
              }
    return render(request, "profile.html", context)

@login_required
def progressbar(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    all_subgoal = Subgoal.objects.all()
    subgoals = all_subgoal.filter(maingoal=goal)
    cant = subgoals.count()
    comp = 0;
    if cant == 0:
        if goal.state == 'done':
            prog = 100
        else:
            prog = 0
    else:
        for subs in subgoals:
            if (subs.state == True):
                comp = comp+1
        prog = (comp * 100)/cant

    return prog