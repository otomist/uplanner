from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', RedirectView.as_view(url='/uplanner/', permanent=True)), #reconsider this
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('schedule.html', views.schedule, name='schedule'),
    path('userprofile.html', views.userprofile, name='userprofile'),
    path('flowchart.html', views.flowchart, name='flowchart')

]