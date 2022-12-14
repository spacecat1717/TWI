from django.urls import path
from . import views

app_name = 'client_interface'

urlpatterns = [
    #CREATION
    path('', views.index, name='index'),
    path('course_creation/', views.course_creation, name='course_creation'),
    path('<slug:course_slug>/course_added/', views.course_added, name='course_added'),
    path('<slug:course_slug>/process_creation/', views.process_creation, name='process_creation'),
    path('<slug:course_slug>/<slug:process_slug>/process_added/', views.process_added, name='process_added'),
    path('<slug:course_slug>/<slug:process_slug>/action_creation/', views.action_creation, name='action_creation'),
    path('<slug:course_slug>/<slug:process_slug>/<slug:action_slug>/action_added/', views.action_added, name='action_added'),
    #EDITING
    path('courses/<slug:course_slug>/edit/', views.course_editing, name='course_editing'),
    path('courses/<slug:course_slug>/<slug:process_slug>/edit/', views.process_editing, name='process_editing'),
    path('courses/<slug:course_slug>/<slug:process_slug>/<slug:action_slug>/edit/', views.action_editing, name='action_editing'),
    #DELETING
    path('courses/<slug:course_slug>/deletion/', views.course_deleting, name='course_deleting'),
    path('courses/<slug:course_slug>/<slug:process_slug>/deletion/', views.process_deleting, name='process_deleting'),
    path('courses/<slug:course_slug>/<slug:process_slug>/<slug:action_slug>/deletion/', views.action_deleting, name='action_deleting'),
    #SHOWING
    path('courses/<slug:course_slug>/', views.course_showing, name='course_showing'),
    path('courses/<slug:course_slug>/<slug:process_slug>/', views.process_showing, name='process_showing'),
    path('courses/<slug:course_slug>/<slug:process_slug>/<slug:action_slug>/', views.action_showing, name='action_showing'),
   

]