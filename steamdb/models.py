#! /usr/bin/python3.7

import datetime

from django.db import models
from django.utils.timezone import now


class SteamDB(models.Model):

    app_id = models.IntegerField("Steam ID")
    app_name = models.CharField("app name", max_length=300, default="NULL")
    app_desc = models.TextField("app glance", max_length=500, default="NULL")
    app_tag = models.TextField("app Tags", max_length=200, default="NULL")
    app_release_date = models.DateTimeField("Release Date", default=now)

    def __str__(self):
        return self.app_name

    def _is_release_recently(self):
        return self.app_release_date >= now() - datetime.timedelta(days=100)
