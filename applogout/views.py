from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from appmodels.models import User

def index(request):
    if 'user_id' in request.session:
        return render (request, 'logout/index.html')
    else:
        return HttpResponseRedirect('/')

@ensure_csrf_cookie
def post(request):
    if 'user_id' not in request.session:
        return JsonResponse({}, status = 403)

    if request.method != 'POST':
        return JsonResponse({}, status = 405)

    try:
        del request.session['user_id']
    except:
        return JsonResponse({}, status = 500)

    return JsonResponse({})
# Create your views here.
