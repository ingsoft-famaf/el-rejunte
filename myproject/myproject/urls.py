"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete, \
    password_reset_done

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'', include('goalsettracker.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/login/$', views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^user/password/reset/$', password_reset, {'post_reset_redirect': '/user/password/reset/done/'}),
    url(r'^user/password/reset/done/$', password_reset_done),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {'post_reset_redirect': '/user/password/done/'}, name='password_reset_confirm'),
    url(r'^user/password/done/$', password_reset_complete),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
