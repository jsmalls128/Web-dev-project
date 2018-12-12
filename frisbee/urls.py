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
    path('on-going-events/', views.onGoingEvents, name='onGoingEvents'),	
    path('schema/', views.schema, name='schema'),
    path('mail/', views.sendMail, name='mail'),	
    path('joinEvent/<int:eventid>', views.joinEvent, name='joinEvent'),
    path('<slug:uid>/<slug:token>', views.confirm, name='confirm'),
]
