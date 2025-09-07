from django.urls import path
from . import views

urlpatterns = [
    path("", views.applicationTracker, name="applicationTracker"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("addApplication", views.addApplication, name="addApplication"),
    path("deleteApplication/<int:app_id>/", views.deleteApplication, name="deleteApplication"),
    path("updateApplication/<int:app_id>/", views.updateApplication, name="updateApplication"),
    path("searchCompanies/", views.searchCompanies, name="searchCompanies"),
    path("createAccount", views.createAccount, name="createAccount")
]
