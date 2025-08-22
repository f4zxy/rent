from django.urls import re_path, include
from . import views


urlpatterns = [
    # Home Page
    re_path(r'^$', views.ok, name='home'),
    
    # Authentication Routes
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^user_login/$', views.user_login, name='user_login'),
    re_path(r'^logout_view/$', views.logout_view, name='logout_view'),
    
    # User Routes
    re_path(r'^profile_view/$', views.profile_view, name='profile_view'),
    re_path(r'^admin_dashboard/$', views.admin_dashboard, name='admin_dashboard'),
]