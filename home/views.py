from django.shortcuts import render
from appmodels.models import User, Release
from appmodels.serializers import UserSerializer, ReleaseSerializer
from datetime import date, timedelta
from django.db.models import Count, Q

# Create your views here.

def index(request):
    seven_days_ago = date.today() - timedelta(7)

    print(seven_days_ago)
    whats_hot = Release.objects.annotate(
        weekly_rating_count=Count('rating', filter=Q(rating__date__gt=seven_days_ago))
    ).filter(weekly_rating_count__gt=0).order_by('-weekly_rating_count')[:3]

    # followed = Connection.objects.filter(follower_id = request.session["id"]).values_list("followee_id", flat=True) # array of all the followed user IDs for the given user
    # followed_ratings = Rating.objects.filter(user_id__in = followed).order_by("-date")[:3]

    return render (request, "home/index.html", {
        'whats_hot': ReleaseSerializer(whats_hot, many=True).data,
        'logged_in': 'user_id' in request.session
    })
