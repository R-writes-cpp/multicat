from django.shortcuts import render
from appmodels.serializers import ReleaseSerializer, RatingSerializer
from django.forms import ModelForm
from appmodels.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['join_date']

@ensure_csrf_cookie
def index(request):
    if request.method == 'GET':
        if 'user_id' in request.session:
            return HttpResponseRedirect('/')
        else:
            return render (request, 'signup/index.html', {
                'logged_in': False
            })
    else:
        return JsonResponse(status = 405)

def post(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            return JsonResponse({}, status = 403) # forbidden from creating a new account if already logged in
        else:
            signup_form = UserForm(request.POST, request.FILES)
            if signup_form.is_valid():
                registered_user = signup_form.save()
                request.session['user_id'] = registered_user.id
                return JsonResponse({'userId': registered_user.id}, status = 201)
            else:
                return JsonResponse({}, status = 400)
    else:
        return JsonResponse(staus = 405)
