"""peering_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views


handler500 = views.handle_500

__patterns = [
    # Include the peering app
    url(r'', include('peering.urls')),

    # Include the peeringdb app
    url(r'', include('peeringdb.urls')),

    # Users login/logout
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # User profile, password, activity
    url(r'^profile/$', views.ProfileView.as_view(), name='user_profile'),
    url(r'^password/$', views.ChangePasswordView.as_view(),
        name='user_change_password'),
    url(r'^activity/$', views.RecentActivityView.as_view(), name='user_activity'),

    # Home
    url(r'^$', views.Home.as_view(), name='home'),

    # setup
    url(r'^setup$', views.Setup.as_view(), name='setup'),

    # Admin
    url(r'^admin/', admin.site.urls),

    # Error triggering
    url(r'^error500/$', views.trigger_500),
]

# Prepend BASE_PATH
urlpatterns = [
    url(r'^{}'.format(settings.BASE_PATH), include(__patterns))
]
