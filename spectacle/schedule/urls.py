from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course-detail')
]