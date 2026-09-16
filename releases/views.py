from django.shortcuts import render
from appmodels.models import Release, Rating, User, DescriptorVote
from appmodels.serializers import ReleaseSerializer, RatingSerializer, DescriptorVoteSerializer
from django.http import HttpResponse
from json import loads

from django.db.models import Avg

# Create your views here.

def overview(request, pk):
    release = Release.objects.get(id = pk)
    ratings = Rating.objects.filter(release__id = pk)
    last_ratings = ratings.order_by('-date')[:5]

    user_rating = 0
    if 'user_id' in request.session:
        try:
            user_rating = Rating.objects.get(release__id = pk, user__id = request.session['user_id']).score
        except Rating.DoesNotExist:
            pass

    return render (request, 'releases/overview.html', {
        'release': ReleaseSerializer(release).data,
        'avg': ratings.aggregate(Avg('score', default = 0))['score__avg'], # annotate for the average rating and then access it from the returned QuerySet
        'rating_count': ratings.count(),
        'last_ratings': RatingSerializer(last_ratings, many=True).data,
        'logged_in': request.session.__contains__('user_id'),
        'user_rating': user_rating
    })

def rate(request, pk):
    if 'user_id' not in request.session:
        return HttpResponse(status = 403)

    if request.method != 'POST':
        return HttpResponse(status = 405)

    Rating.objects.update_or_create(
        user_id = request.session['user_id'],
        release_id = pk,
        defaults = {'score': request.body, 'date': Rating._meta.get_field('date').get_default()}
    )

    return HttpResponse(status = 201)

def vote(request, pk):
    if 'user_id' not in request.session:
        return HttpResponse(status = 403)

    if request.method == 'GET':
        release = Release.objects.get(id = pk)
        descriptor_votes = DescriptorVote.objects.filter(user__id = request.session['user_id'], release__id = pk)

        return render(request, 'releases/vote.html', {
            'release': ReleaseSerializer(release).data,
            'descriptor_votes': DescriptorVoteSerializer(descriptor_votes, many=True).data,
            'logged_in': True
        })
    elif request.method == 'POST':
        descriptor_votes = loads(request.body)
        for i in range (len (descriptor_votes)):
            if descriptor_votes[i] != 0:
                DescriptorVote.objects.update_or_create(
                    user_id = request.session['user_id'],
                    release_id = pk,
                    descriptor = i,
                    defaults = {'score': descriptor_votes[i]}
                )

        return HttpResponse(status = 201)
    else:
        return HttpResponse(status = 403)
