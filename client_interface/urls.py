from django.urls import path
from . import views

app_name = 'client_interface'

urlpatterns = [
    path('', views.index, name='index'),
    path('course_creation/', views.course_creation, name='course_creation'),
    path('<slug:course_slug>/course_added/', views.course_added, name='course_added'),
    path('<slug:course_slug>/action_creation/', views.action_creation, name='action_creation'),
    path('<slug:course_slug>/<slug:action_slug>/action_added/', views.action_added, name='action_added'),
    path('<slug:course_slug>/step_creation/', views.step_creation, name='step_creation'),
    path('<slug:course_slug>/<slug:step_slug>/step_added/', views.step_added, name='step_added'),
]