from django.shortcuts import render
from appmodels.models import Release, Rating, Review, User, DescriptorVote, Comment
from appmodels.serializers import ReleaseSerializer, RatingSerializer, ReviewSerializer, CommentSerializer, DescriptorVoteSerializer
from django.http import HttpResponse
from json import loads

from django.db.models import Avg
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

@ensure_csrf_cookie
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

    if int(request.body) < 1 or int(request.body) > 10:
        return HttpResponse(status = 400)

    Rating.objects.update_or_create(
        user_id = request.session['user_id'],
        release_id = pk,
        defaults = {'score': request.body, 'date': Rating._meta.get_field('date').get_default()}
    )

    return HttpResponse(status = 201)

@ensure_csrf_cookie
def vote(request, pk):
    if 'user_id' not in request.session:
        return HttpResponse(status = 403)

    if request.method != 'GET':
        return HttpResonse (status = 405)

    release = Release.objects.get(id = pk)
    descriptor_votes = DescriptorVote.objects.filter(user__id = request.session['user_id'], release__id = pk)

    return render(request, 'releases/vote.html', {
        'release': ReleaseSerializer(release).data,
        'descriptor_votes': DescriptorVoteSerializer(descriptor_votes, many=True).data,
        'logged_in': True
    })

def vote_post(request, pk):
    if request.method != 'POST':
        return HttpResponse(status = 405)

    descriptor_votes = loads(request.body)
    for i in range (len (descriptor_votes)):
        if descriptor_votes[i] == 0: # if this descriptor wasn't voted on...
            continue
        elif descriptor_votes[i] < 1 or descriptor_votes[i] > 4 or int(descriptor_votes[i]) != descriptor_votes[i]: # if the descriptor was voted on (i.e. the score wasn't equal to 0) BUT it's outside of the valid bounds/isn't an integer, then...
            return HttpResponse(status = 400) # it's invalid! return HTTP code 400
        else:
            DescriptorVote.objects.update_or_create(
                user_id = request.session['user_id'],
                release_id = pk,
                descriptor = i,
                defaults = {'score': descriptor_votes[i]}
            )

    return HttpResponse(status = 201)

@ensure_csrf_cookie
def reviews(request, pk):
    if request.method != 'GET':
        return HttpResponse(status = 405)

    release = Release.objects.get(id = pk)

    last_reviews = Review.objects.filter(rating__release__id = pk).order_by('-rating__date')[:10]

    ratings = Rating.objects.filter(release__id = pk)

    return render(request, 'releases/reviews.html', {
        'release': ReleaseSerializer(release).data,
        'last_reviews': ReviewSerializer(last_reviews, many=True).data,
        'avg': ratings.aggregate(Avg('score', default = 0))['score__avg'],
        'rating_count': ratings.count(),
        'logged_in': 'user_id' in request.session
    })

def review_post(request, pk):
    if request.method != 'POST':
        return HttpResponse(status = 405)
    if 'user_id' not in request.session:
        return HttpResponse(status = 403)

    try:
        user_rating = Rating.objects.get(user__id = request.session['user_id'], release__id = pk)
    except Rating.DoesNotExist: # need an associated rating to make a review
        return HttpResponse(status = 403)

    user_review = Review.objects.update_or_create(
        rating = user_rating,
        defaults = {'text': loads(request.body)}
    )

    return HttpResponse(status = 201)

@ensure_csrf_cookie
def comments(request, pk):
    if request.method != 'GET':
        return HttpResponse(status = 403)

    release = Release.objects.get(id = pk)

    last_comments = Comment.objects.filter(release__id = pk).order_by('-date')[:10]

    ratings = Rating.objects.filter(release__id = pk)

    return render(request, 'releases/comments.html', {
        'release': ReleaseSerializer(release).data,
        'last_comments': CommentSerializer(last_comments, many=True).data,
        'avg': ratings.aggregate(Avg('score', default = 0))['score__avg'],
        'rating_count': ratings.count(),
        'logged_in': 'user_id' in request.session
    })

def comment_post(request, pk):
    if request.method != 'POST':
        return HttpResponse(status = 405)
    if 'user_id' not in request.session:
        return HttpResponse(status = 403)

    user_comment = Comment.objects.create(
        user_id = request.session['user_id'],
        release_id = pk,
        text = loads(request.body)
    )

    return HttpResponse(status = 201)
