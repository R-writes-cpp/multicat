from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/vote/post", views.vote_post, name="vote_post"),
    path("<int:pk>/vote", views.vote, name="vote"),
    path("<int:pk>/rate", views.rate, name="rate"),
    path("<int:pk>/reviews/post", views.review_post, name="review_post"),
    path("<int:pk>/reviews", views.reviews, name="reviews"),
    path("<int:pk>/comments/post", views.comment_post, name="comment_post"),
    path("<int:pk>/comments", views.comments, name="comments"),
    path("<int:pk>", views.overview, name="overview")
]
