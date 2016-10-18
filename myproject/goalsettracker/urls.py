from django.conf.urls import url
from . import views


# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/register$', views.register, name='register'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^register/success/$', views.register_success, name='register_success'),
]
