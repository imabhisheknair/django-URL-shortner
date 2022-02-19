from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.land_page),
    path('login', views.login_page),
    path('signup', views.signup),
    re_path(r'^l/(?P<key>\w+)/$', views.redirect_to),
    path('dashboard', views.user_dashboard),
    path('logout', views.logout_now),
    path('login_handle', views.login_handle),
]
