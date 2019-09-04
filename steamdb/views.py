from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader

from .models import SteamDB


def game_summary(request):

    template = loader.get_template("steamdb/summary.html")
    game_list = SteamDB.objects.all()
    context = {
        'game_list': game_list
    }

    return HttpResponse(template.render(context, request))


def game_detail(request, game_id):
    template = loader.get_template("steamdb/detail.html")
    game = get_object_or_404(SteamDB, game_id=game_id)
    context = {
        "game": game
    }
    return HttpResponse(template.render(context, request))
