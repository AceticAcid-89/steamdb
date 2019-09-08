#! /usr/bin/python3.7

from collections import deque

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse

from .forms import AppEditForm
from .models import SteamDB
from .utils.app_operator import AppOperator


def app_summary(request):
    app_deque = deque(maxlen=50)
    template = loader.get_template("steamdb/summary.html")
    app_list = SteamDB.objects.order_by("app_id")
    app_deque.extend(app_list)
    context = {
        'app_list': app_deque
    }

    return HttpResponse(template.render(context, request))


def app_detail(request, app_id):
    template = loader.get_template("steamdb/detail.html")
    app = get_object_or_404(SteamDB, app_id=app_id)
    form = AppEditForm()
    context = {
        "app": app,
        "app_edit_form": form
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


def app_catch(request):
    app_opt = AppOperator()
    app_list = app_opt.get_app_list()
    for app in app_list:
        try:
            app_model = SteamDB(app_id=app["appid"], app_name=app["name"])
            app_model.save()
        except Exception:
            continue
    return HttpResponseRedirect(reverse('steamdb:app_summary', args=()))


def auto_update_app(request, app_id):
    app_obj = get_object_or_404(SteamDB, app_id=app_id)
    app_opt = AppOperator()
    data = app_opt.get_app_info(app_id).get(str(app_id)).get("data")
    app_obj.app_desc = data.get("short_description")

    print(data)
    return HttpResponseRedirect(reverse('steamdb:app_summary', args=()))