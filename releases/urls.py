from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/vote", views.vote, name="vote"),
    path("<int:pk>/rate", views.rate, name="rate"),
    path("<int:pk>", views.overview, name="overview")
]
