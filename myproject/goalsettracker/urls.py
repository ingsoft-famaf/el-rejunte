from django.conf.urls import url

from . import views
from .views import *

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/order_by=(?P<order_by>[A-Za-z]+)$', views.home, name='home'),
    url(r'^login/register$', Register.as_view(), name='register'),
    url(r'^register/', Register.as_view(), name='register'),
    url(r'^deactivate_user$', views.deactivate_user, name='deactivate_user'),
    url(r'^addgoal/', views.addgoal, name='addgoal'),
    url(r'^goal/(?P<goal_id>[0-9]+)/modify_goal/$', views.addgoal, name='modify_goal'),
    url(r'^profile/edit/(?P<myuser_id>[0-9]+)/$', views.add_profile_photo, name='modify_photo'),
    url(r'^goalfilter/', views.goalfilter, name='goalfilter'),
    url(r'^goal/(?P<goal_id>[0-9]+)$', views.goaldetail, name='goaldetail'),
    url(r"^goal/(?P<goal_id>[0-9]+)/completegoal/$", views.completegoal, name='completegoal'),
    url(r'^goal/(?P<goal_id>[0-9]+)/addsubgoal/$', views.addsubgoal, name='addsubgoal'),
    url(r'^goal/(?P<goal_id>[0-9]+)/addmoretime/$', views.addmoretime, name='addmoretime'),
    url(r'^goal/(?P<goal_id>[0-9]+)/delete_goal/$', views.delete_goal, name='delete_goal'),
    url(r"^goal/(?P<goal_id>[0-9]+)/(?P<comment_id>[0-9]+)/delete_comment/$", views.delete_confirm_comment, name='delete_comment'),
    url(r"^profile/delete(?P<myuser_id>[0-9]+)/$", views.delete_confirm_photo, name='delete_photo'),
    url(r'^completesubgoal/(?P<goal_id>[0-9]+)/(?P<subgoal_id>[0-9]+)$', views.completesubgoal, name='completesubgoal'),
    url(r'^deletesubgoal/(?P<goal_id>[0-9]+)/(?P<subgoal_id>[0-9]+)$', views.deletesubgoal, name='deletesubgoal'),
    url(r'^miscategorias/(?P<category_id>[0-9]+)/delete_category/$', views.delete_category, name='delete_category'),
    url(r'^allgoaldetail/', views.allgoaldetail, name='allgoaldetail'),
    url(r'^newcategory/', views.new_category, name='newcategory'),
    url(r'^miscategorias/(?P<category_id>[0-9]+)/edit_category', views.new_category, name='newcategory'),
    url(r'^miscategorias/', views.miscategorias, name='miscategorias'),
    url(r'^profile/', views.profile),
    # url(r'^miscategorias/(?P<category_id>[0-9]+)/delete', views.delete_category, name='delete_category'),
    url(r'^add_photo/$', views.add_profile_photo, name='add_profile_photo'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),

]
