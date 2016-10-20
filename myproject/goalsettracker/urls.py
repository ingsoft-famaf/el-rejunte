from django.conf.urls import url
from . import views
from goalsettracker.views import Register, AddMeta


# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/register$', Register.as_view(), name='register'),
    url(r'^register/', Register.as_view(), name='register'),
    url(r'^home/addmeta/', AddMeta.as_view(), name='addmeta'),
    #url(r'^register/$', views.register, name = 'register'),
]
