from django.shortcuts import render
from appmodels.serializers import ReleaseSerializer, RatingSerializer
from django.forms import ModelForm
from appmodels.models import User
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['join_date']

def index(request):
    if 'user_id' in request.session:
        return HttpResponseRedirect('/')
    else:
        return render (request, 'signup/index.html', {
            'logged_in': False
        })

def post(request):
    if 'user_id' in request.session:
        return JsonResponse({}, status = 403) # forbidden from creating a new account if already logged in
    elif request.method != 'POST':
        return JsonResponse({}, status = 405) # this view is exclusively used to handle POST sign-up requests
    else:
        signup_form = UserForm(request.POST, request.FILES)
        if signup_form.is_valid():
            registered_user = signup_form.save()
            return JsonResponse({'userId': registered_user.id}, status = 201)
        else:
            return JsonResponse({}, status = 400)
