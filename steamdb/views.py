from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse

from .models import SteamDB


def app_summary(request):

    template = loader.get_template("steamdb/summary.html")
    app_list = SteamDB.objects.all()
    context = {
        'app_list': app_list
    }

    return HttpResponse(template.render(context, request))


def app_detail(request, app_id):
    template = loader.get_template("steamdb/detail.html")
    app = get_object_or_404(SteamDB, app_id=app_id)
    context = {
        "app": app
    }
    return HttpResponse(template.render(context, request))


def app_edit(request, app_id):
    app_obj = get_object_or_404(SteamDB, app_id=app_id)
    for key, value in request.POST.items():
        if not hasattr(app_obj, key):
            continue
        setattr(app_obj, key, value)
    app_obj.save()

    return HttpResponseRedirect(reverse('steamdb:app_detail', args=(app_id,)))


def app_add(request):
    app_obj = SteamDB()
    for key, value in request.POST.items():
        if not hasattr(app_obj, key):
            continue
        setattr(app_obj, key, value)
    app_obj.save()

    return HttpResponseRedirect(reverse('steamdb:app_summary', args=()))


def app_delete(request, app_id):
    app_obj = get_object_or_404(SteamDB, app_id=app_id)
    app_obj.delete()
    return HttpResponseRedirect(reverse('steamdb:app_summary', args=()))
