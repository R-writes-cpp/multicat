from django.shortcuts import render

from appmodels.models import Release
from appmodels.serializers import ReleaseSerializer

from utils import levenshtein, priority_queue

# Create your views here.

def searchapp(request):
    query = request.GET['q']

    releases_with_levenshtein = list (map (lambda r : (r, levenshtein(query, r.title)), Release.objects.all()))
    close_releases = list (filter (lambda p : p[1] / len(query) < 0.6, releases_with_levenshtein))

    pq_levenshtein = priority_queue(
        close_releases,
        weight=lambda r : r[1],
        copy=False,
        desc=False
    )

    top_5 = pq_levenshtein.get_top_n(5)

    return render (request, 'search/index.html', {
        'top_5_data': ReleaseSerializer(list (map (lambda x : x[0], top_5)), many=True).data,
        'logged_in': 'user_id' in request.session
    })
