from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import CreateView

from .forms import *


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
    return render_to_response(
        'home.html',
        {'user': request.user}
    )


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
        #if request.method == "POST":
        user_form = DeactivateUserForm(request.POST, instance=user)
        if user_form.is_valid():
            user.is_active = False
            user.save()
            # es necesario mandar un mail?
            # email_user(subject, message, from_email=None, **kwargs)
        return render(request, "deactivate_user.html", {"user_form": user_form, })
