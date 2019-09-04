#! /usr/bin/python3.7

import datetime

from django.db import models
from django.utils.timezone import now


class SteamDB(models.Model):

    game_id = models.IntegerField("Steam ID", max_length=30)
    game_name = models.CharField("Game name", max_length=300)
    game_desc = models.TextField("Game glance", max_length=500, default="")
    game_tag = models.TextField("Game Tags", max_length=200, default="")
    game_release_date = models.DateTimeField("Release Date", default=now)

    def __str__(self):
        return self.game_name

    def _is_release_recently(self):
        return self.game_release_date >= now() - datetime.timedelta(days=100)
