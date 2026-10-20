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
