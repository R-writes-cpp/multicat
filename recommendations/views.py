from django.shortcuts import render
from django.http import HttpResponseRedirect
from appmodels.models import Release, Rating, DescriptorVote
from appmodels.serializers import ReleaseSerializer
from django.db.models import Avg, StdDev, Q

from utils import priority_queue, clamp
from appmodels.models import get_ranking_weight

def get_std_dev_from_mean(rating): # calculates how many standard deviations the given rating is above or below the mean
    release_ratings = Rating.objects.filter(release__id = rating.release.id)
    rating_stats = release_ratings.aggregate(avg=Avg('score', default=0), std_dev=StdDev('score', default=0))

    return ((rating.score - rating_stats['avg']) / rating_stats['std_dev']) if rating_stats['std_dev'] != 0 else 0

DESCRIPTOR_AVG_ARGS = {'{}_avg'.format(d): Avg('score', default=0, filter=Q(descriptor = d)) for d in range(18)} # dictionary comprehension which looks something like: {'0_avg': [AVERAGE SCORE FILTERED FOR DESCRIPTOR 0, '1_avg': [DITTO BUT FOR DESCRIPTOR 1], ...}. double splat operator converts this into a bunch of kwargs which can be passed to the aggregate method

def get_descriptor_avgs(release_id):
    votes = DescriptorVote.objects.filter(release__id = release_id)

    avg_aggregation = votes.aggregate(**DESCRIPTOR_AVG_ARGS)

    return [avg_aggregation['{}_avg'.format(d)] for d in range(18)]

def get_descriptor_profile(user_id):
    weighted_sums = [0 for _ in range(18)]
    freqs = [0 for _ in range(18)]

    user_ratings = Rating.objects.filter(user__id = user_id)

    for rating in user_ratings:
        std_devs_from_mean = get_std_dev_from_mean(rating)
        descriptor_avgs = get_descriptor_avgs(rating.release.id)

        for d in range(18):
            current_avg = descriptor_avgs[d]
            if current_avg != 0:
                weighted_sums[d] += std_devs_from_mean * (current_avg - 2.5) / 2 # latter part of the product quantifies how far above average the current descriptor is. we scale the result down by 2 so that we can achieve a higher resolution (remember that the value is clamped to the range [1, 4] in the end)
                freqs[d] += 1

    return [(clamp (1, 2.5 + weighted_sums[d] / freqs[d], 4) if freqs[d] != 0 else 2.5) for d in range(18)]

def get_mean_difference(user_descriptor_profile, descriptor_avgs):
    diff_sum = 0
    count = 0

    for d in range(18):
        if descriptor_avgs[d] != 0: # if the descriptor has been voted on in the given release...
            diff_sum += (descriptor_avgs[d] - user_descriptor_profile[d]) ** 2
            count += 1

    return (diff_sum / count) * (18 / count) ** 0.3 if count != 0 else 2.25 # square of half the maximum possible difference

def get_recommendation_score(profile, release):
    avgs = get_descriptor_avgs(release.id)

    rw = get_ranking_weight(release)

    return rw ** 2 / (get_mean_difference(profile, avgs) + 1) # square the ranking weight so that quality has more effect on final recommendation score than taste affinity; add 1 so that the reciprocal growth is steadier/more gradual.

def index(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect ('/login')

    profile = get_descriptor_profile(request.session['user_id'])

    pq_recs = priority_queue (
        list (Release.objects.all()),
        weight=lambda r : get_recommendation_score(profile, r)
    )

    top_5 = pq_recs.get_top_n(5)

    return render (request, 'recommendations/index.html', {
        'top_5_data': ReleaseSerializer(top_5, many=True).data
    })
