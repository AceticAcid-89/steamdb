#! /usr/bin/python3.7

from collections import deque
from datetime import datetime
from io import BytesIO
from PIL import Image
import requests


from django.core.files.storage import FileSystemStorage
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
    app_list = SteamDB.objects.order_by("-app_id")
    app_deque.extend(app_list)
    context = {
        'app_list': app_deque
    }

    return HttpResponse(template.render(context, request))


def app_detail(request, app_id):
    template = loader.get_template("steamdb/detail.html")
    app_obj = get_object_or_404(SteamDB, app_id=app_id)

    app_opt = AppOperator()
    data = app_opt.get_app_info(app_id).get(str(app_id)).get("data")
    if not app_obj.app_info_complete:
        app_obj.app_desc = data.get("short_description")
        # update header image
        thumbnail_url = data.get("header_image").replace(" ", "")
        r = requests.get(thumbnail_url)
        name = "steamdb/static/documents/header_%s.jpg" % app_id
        image = Image.open(BytesIO(r.content))
        image.save(name)
        app_obj.app_thumbnail = name.replace("steamdb/static/", "")
        app_obj.app_publisher = data.get("publishers")
        app_obj.app_developer = data.get("developers")
        app_obj.app_tag = "/".join([item["description"] for item in data.get("categories")])
        app_obj.app_price = data.get("price_overview", {}).get("final", 0) / 100
        date = data.get("release_date", {}).get("date")
        if date:
            dt = datetime.strptime(date, "%d %b, %Y")
            app_obj.app_release_date = dt.strftime("%Y-%m-%d")

        app_obj.app_info_complete = True
        app_obj.save()

    form = AppEditForm()
    context = {
        "app": app_obj,
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
    app_thumbnail = request.FILES.get("app_thumbnail")
    if app_thumbnail:
        fs = FileSystemStorage()
        name = "steamdb/static/documents/header_%s.%s" %\
               (app_id, app_thumbnail.name.split(".")[-1])
        filename = fs.save(name, app_thumbnail)
        app_obj.app_thumbnail = fs.url(filename).replace("steamdb/static/", "")
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
