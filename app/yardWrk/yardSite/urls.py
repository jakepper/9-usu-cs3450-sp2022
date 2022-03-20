import imp
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerDashboard, name="customerDashboard"),
    path('job/create', views.create_job_post, name="job post creations")
]