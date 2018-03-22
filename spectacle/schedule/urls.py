from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', RedirectView.as_view(url='/uplanner/', permanent=True)), #reconsider this
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('schedule/', views.schedule, name='schedule'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('flowchart/', views.flowchart, name='flowchart')
]