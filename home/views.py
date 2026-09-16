from django.shortcuts import render
from appmodels.models import User, Rating, Release, Creator, Connection

# Create your views here.

def index(request):
    whats_hot_releases = list (map(
        lambda r: Release.objects.get(id = r.release_id),
        Rating.objects.order_by("-date")[:3]
    ))

    whats_hot_creators = list (map(
        lambda r: Creator.objects.get(id = r.creator1_id),
        whats_hot_releases
    ))

    followed = Connection.objects.filter(follower_id = request.session["id"]).values_list("followee_id", flat=True) # array of all the followed user IDs for the given user
    followed_ratings = Rating.objects.filter(user_id__in = followed).order_by("-date")[:3]

    return render (request, "home/index.html", {
        "user": User.objects.get(id = request.session["id"]) if request.session.has_key("id") else None,
        "whats_hot": [{
            "creator": whats_hot_creators[i],
            "release": whats_hot_releases[i]
        } for i in range(len (whats_hot_releases))]

    })
