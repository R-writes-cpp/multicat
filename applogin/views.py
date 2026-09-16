from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from appmodels.models import User

def index(request):
    if 'user_id' in request.session:
        return HttpResponseRedirect('/users')
    else:
        return render (request, 'login/index.html')

@ensure_csrf_cookie
def post(request):
    if 'user_id' in request.session:
        return JsonResponse({}, status = 403)

    if request.method != 'POST':
        return JsonResponse({}, status = 405)

    try:
        user_id = User.objects.get(username = request.body.decode('utf-8')).id
        request.session['user_id'] = user_id
    except User.DoesNotExist:
        return JsonResponse({}, status = 404)

    return JsonResponse({})
# Create your views here.
