from django.shortcuts import render

from appmodels.models import Release
from appmodels.serializers import ReleaseSerializer

from utils import levenshtein, priority_queue, get_top_n

# Create your views here.

def searchapp(request):
    query = request.GET['q']

    releases_with_levenshtein = list (map (lambda r : (r, levenshtein(query, r.title)), Release.objects.all()))

    close_releases = list (filter (lambda p : p[1] / len(query) < 0.6, releases_with_levenshtein))

    pq_levenshtein = priority_queue(
        close_releases,
        cmp=staticmethod (lambda parent, child : parent[1] < child[1])
    )

    top_5 = get_top_n(5, pq_levenshtein, staticmethod(lambda p : p[0]))

    return render (request, 'search/index.html', {
        'top_5_data': ReleaseSerializer(top_5, many=True).data
    })
