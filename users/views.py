from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from appmodels.models import User, Rating, Release, Creator, Connection
from appmodels.serializers import UserSerializer, RatingSerializer
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.
def profile(request, pk):
    user_obj = User.objects.get(id = pk)
    last_ratings = Rating.objects.filter(user__id = pk).order_by("-date")[:5]

    return render (request, 'users/profile.html', {
        'user_data': UserSerializer(user_obj).data,
        'last_ratings_data': RatingSerializer(last_ratings, many=True).data,
        'logged_in': request.session.__contains__('user_id')
    })

def get_own_profile(request):
    if 'user_id' in request.session:
        return HttpResponseRedirect('/users/{}'.format(request.session['user_id']))
    else:
        return HttpResponseRedirect('/')
"""
class get_user(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def get_ratings(request, pk):
    if request.method == "GET":
        num_of_ratings = request.query_params.get('n', -1)
        if num_of_ratings == -1:
            ratings = Rating.objects.filter(user__id = pk).order_by("-date")
        else:
            ratings = Rating.objects.filter(user__id = pk).order_by("-date")[:num_of_ratings]

        serializer = UserSerializer(ratings, many=True)
        return Response(serializer.data)

    return Response()
"""

"""
def profile(request, user_id):
    try:
        user = User.objects.get(id = user_id)

        last_three_ratings = Rating.objects.order_by("-date")[:3]
        last_three_ratings_bundle = ratings_to_bundle(last_three_ratings, bundle_mode.RELEASE | bundle_mode.CREATOR | bundle_mode.RATING)

    except User.DoesNotExist:
        raise Http404("User ID is invalid.")

    return render(request, "user/profile.html", {
        "user": user,
        "rating_bundle": last_three_ratings_bundle
    })

def ratings(request, user_id):
    try:
        user = User.objects.get(id = user_id)

        last_ratings = Rating.objects.order_by("-date")
        last_ratings_bundle = ratings_to_bundle(last_ratings, bundle_mode.RELEASE | bundle_mode.CREATOR | bundle_mode.RATING)

    except User.DoesNotExist:
        raise Http404("User ID is invalid.")

    return render(request, "user/ratings.html", {
        "user": user,
        "rating_bundle": last_ratings_bundle
    })

def follow(request, followee_id):
    if request.method != "POST":
        return HttpResponse(status = 400)

    try:
        _ = Connection.objects.create(follower_id = request.session["id"], followee_id = followee_id)
    except:
        return HttpResponse(status = 401)
    else:
        return HttpResponse(status = 201)
"""
