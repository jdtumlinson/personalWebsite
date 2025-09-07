from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="homePage"),
    path("about", views.aboutPage, name="about"),
    path("projects", views.projectsPage, name="projects"),
    path("contact", views.contactPage, name="contact"),
]
