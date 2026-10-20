from django.shortcuts import render
from appmodels.models import Release, Rating
from appmodels.serializers import ReleaseSerializer
from django.db.models import Avg, Q
from math import log10, sqrt
from json import loads

from utils import priority_queue
from appmodels.models import get_ranking_weight

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
        weight=lambda r : get_ranking_weight(r)
    )

    top_5 = pq_ranking.get_top_n(5)

    return render (request, 'rankings/index.html', {
        'top_5_data': ReleaseSerializer(top_5, many=True).data,
        'logged_in': True
    })
