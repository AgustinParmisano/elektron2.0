# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import User as ElektronUser
from django.views import generic
from django.views.generic import FormView, RedirectView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    model = ElektronUser

    def get(self, request, *args, **kwargs):
        """Return all elektronusers."""
        return JsonResponse({'elektronusers': list(map(lambda x: x.username, ElektronUser.objects.all()))})

class DetailView(generic.DetailView):
    model = ElektronUser

    def get(self, request, *args, **kwargs):
        """Return the selected by id elektronusers."""
        try:
            return JsonResponse({'elektronuser': ElektronUser.objects.get(id=kwargs["pk"]).username})
        except Exception as e:
            print "Some error ocurred getting Single ElektronUser with id: " + str(kwargs["pk"])
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class LoginView(FormView):

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                user_object = ElektronUser.objects.get(username=username)
                request.session.set_expiry(86400) #sets the exp. value of the session
                login(request, user) #the user is now logged inelse:
                print "User "+ user.username +" login success!"
                print "request.user: " + str(request.session)
                print "autenticated: " + str(request.user.is_authenticated())
                print user_object.username
                request.session['username'] = user_object.username
                print "request.session: " + str(request.session['username'])
                message = {"key":"value"}
                response = JsonResponse({'user': user_object.username})
                print("response.cookies")
                print(dir(response.cookies))
                return response
                #response = HttpResponse(msg=message,status=200)
                #response.set_cookie('name','pepe',7) #key,value,days_expire
                #return response
        print "User or password does not match"
        return HttpResponse(status=500)
        #return HttpResponseRedirect(settings.LOGIN_URL)

class LogoutView(generic.DetailView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse(status=200)
