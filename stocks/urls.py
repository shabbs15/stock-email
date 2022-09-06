from django.urls import path

from . import views

urlpatterns = [
    path("enter/", views.index, name="index"),
    path("wait", views.wait, name="wait"),
    path("authorisation/<authid>/", views.authorisation, name="authorisation"),
    path("app/", views.app, name="app")
]
