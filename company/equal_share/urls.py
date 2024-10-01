from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('startups/', StartupListView.as_view(), name='startup_list'),
    path('startups/<int:pk>/', StartupDetailView.as_view(), name='startup_detail'),
    path('startups/<int:pk>/invest/', invest_in_startup, name='invest_in_startup'),
    path('login/',auth_views.LoginView.as_view(), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(), name = 'logout'),
    path('my-investments/', my_investments, name = 'my_investments'),
]