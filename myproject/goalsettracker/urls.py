from django.conf.urls import url
from . import views
from .views import *


# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/register$', Register.as_view(), name='register'),
    url(r'^register/', Register.as_view(), name='register'),
    url(r'^deactivate_user$', deactivate_user, name='deactivate_user'),
    url(r'^addgoal/', AddGoal.as_view() , name='addgoal'),
    url(r'^goal/(?P<goal_id>[0-9]+)$', views.goaldetail, name='goaldetail'),
    url(r'^goal/(?P<goal_id>[0-9]+)/addsubgoal/$', views.addsubgoal, name='addsubgoal'),
    url(r'^allgoaldetail/', views.allgoaldetail, name='allgoaldetail'),
    url(r'^newcategory/', NewCategory.as_view(), name='newcategory'),
    url(r'^miscategorias/', views.miscategorias, name='miscategorias'),

    
]
