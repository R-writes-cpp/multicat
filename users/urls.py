from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>", views.profile, name="profile"),
    path("", views.get_own_profile, name="get_own_profile")
    # path("<int:pk>/ratings", views.get_ratings, "get_ratings")
]

""",
path("<int:user_id>/follow", views.follow, name="follow"),
path("<int:user_id>/ratings", views.ratings, name="ratings")
"""
