#from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect, render_to_response
from django.contrib import auth

#class IndexView(TemplateView):
def indexview(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def logoutview(request):
    auth.logout(request)
    return HttpResponseRedirect('/loggedout/')

def loggedoutview(request):
    return render_to_response('logout.html')

def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
        return view(request, *args, **kwargs)
    return new_view