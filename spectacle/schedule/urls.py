from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', RedirectView.as_view(url='/uplanner/', permanent=True)), #reconsider this
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/ajax/add', views.add_section, name='add_section'),
    path('schedule/ajax/del', views.del_section, name='del_section'),
    path('schedule/make_tab_content/', views.make_tab_content, name='make_tab_content'),
    path('profile/', views.profile, name='profile'),
    path('prereqs/', views.prereqs, name='prereqs'),
]