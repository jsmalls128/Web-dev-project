from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/team', views.createTeam, name='createTeam'),
    path('profile/event', views.createEvent, name='createEvent'),
    path('event/<int:eventid>', views.viewEvent, name='viewEvent'),
    path('mail/', views.sendMail, name='mail'),
]
