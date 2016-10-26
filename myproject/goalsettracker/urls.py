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
    url(r'^goaldetail/', views.goaldetail, name='goaldetail'),
    url(r'^newcategory/', NewCategory.as_view(), name='newcategory'),

]
