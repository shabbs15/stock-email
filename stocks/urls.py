from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.registerLogin, name="register"),
    path("login/", views.registerLogin, name="login"),
    path("authorisation/<authid>/", views.authorisation, name="authorisation"),
    path("app/", views.app, name="app"),
    path("logout/", views.logout, name="logout")
]
