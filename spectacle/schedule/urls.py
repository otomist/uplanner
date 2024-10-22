from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', RedirectView.as_view(url='/uplanner/', permanent=True)), #reconsider this
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/ajax/add', views.add_section, name='add_section'),
    path('schedule/ajax/del', views.del_section, name='del_section'),
    path('schedule/ajax/schedule', views.schedule_courses, name='schedule_courses'),
    path('schedule/make_tab_content/', views.make_tab_content, name='make_tab_content'),
    path('schedule/ajax/delete_tab/', views.delete_tab, name='delete_tab'),
    path('schedule/make_current_course/', views.make_current_course, name='make_current_course'),
    path('schedule/make_current_courses/', views.make_current_courses, name='make_current_courses'),
    path('schedule/ajax/make_user_event/', views.make_user_event, name='make_user_event'),
    path('schedule/ajax/make_schedule/', views.make_schedule, name='make_schedule'),
    path('schedule/ajax/del_schedule/', views.del_schedule, name='del_schedule'),
    path('schedule/ajax/change_schedule/', views.change_schedule, name='change_schedule'),
    path('schedule/ajax/toggle_filters/', views.toggle_filters, name='toggle_filters'),
    path('schedule/ajax/change_schedulecourse_color/', views.change_schedulecourse_color, name='change_schedulecourse_color'),
    path('profile/', views.profile, name='profile'),
    path('prereqs/', views.prereqs, name='prereqs'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('prereqs/course/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
]