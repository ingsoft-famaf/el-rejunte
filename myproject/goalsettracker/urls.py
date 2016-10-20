from django.conf.urls import url
from . import views
from goalsettracker.views import Register, AddGoal


# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/register$', Register.as_view(), name='register'),
    url(r'^register/', Register.as_view(), name='register'),
    url(r'^home/addgoal/', AddGoal.as_view(), name='addgoal'),
    url(r'^home/goaldetail/', views.goaldetail, name='goaldetail'),
    #url(r'^register/$', views.register, name = 'rgister'),
]
