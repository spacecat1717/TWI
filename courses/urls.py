from django.urls import path
from . import views

app_name='courses'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('courses_list/', views.courses_list, name='courses_list'),
    path('<slug:course_slug>/', views.course_view, name='course_view'),
    path('<slug:course_slug>/<slug:action_slug>/', views.action_view, name='action_view'),
    path('<slug:course_slug>/<slug:action_slug>/<slug:step_slug>/', views.step_view, name='step_view'),
    
]