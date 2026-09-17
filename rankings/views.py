from django.shortcuts import render
from appmodels.models import Release, Rating
from appmodels.serializers import ReleaseSerializer
from django.db.models import Avg, Q
from math import log10, sqrt
from json import loads

from utils import priority_queue, get_top_n

# Create your views here.
def ranking_weight(r):
    release_ratings = Rating.objects.filter(release__id = r.id)
    avg_rating = release_ratings.aggregate(Avg('score', default=0))['score__avg']

    return avg_rating * sqrt(log10(release_ratings.count() + 1))

def index(request):
    filtered_releases = Release.objects.all()
    if 'year' in request.GET:
        print(request.GET['year'])
        filtered_releases = filtered_releases.filter(release_date__year = request.GET['year'])

    if 'descriptors' in request.GET:
        descriptors = loads(request.GET['descriptors'])
        for d in descriptors:
            descriptor_avg = Avg('descriptorvote__score', filter=Q(descriptorvote__descriptor = d))
            filtered_releases = filtered_releases.annotate(**{'{}_avg'.format(d): descriptor_avg})

        descriptor_filter = Q()
        for d in descriptors:
            descriptor_filter = descriptor_filter & Q(**{'{}_avg__gt'.format(d): 2})

        filtered_releases = filtered_releases.filter(descriptor_filter)

    pq_ranking = priority_queue (
        list(filtered_releases),
        cmp=lambda parent, child : ranking_weight(parent) > ranking_weight(child)
    )

    top_5 = get_top_n(5, pq_ranking)

    return render (request, 'rankings/index.html', {
        'top_5_data': ReleaseSerializer(top_5, many=True).data,
        'logged_in': 'user_id' in request.session
    })
