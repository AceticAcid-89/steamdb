#! /usr/bin/python3.7

import datetime

from django.db import models
from django.utils.timezone import now


class SteamDB(models.Model):

    app_id = models.IntegerField("Steam ID")
    app_name = models.CharField("app name", max_length=300, default="NULL")
    app_desc = models.TextField("app glance", max_length=500, default="NULL")
    app_publisher = models.CharField("app publisher", max_length=200, default="NULL")
    app_developer = models.CharField("app developer", max_length=200, default="NULL")
    app_history_reviews = models.TextField("app history reviews", max_length=500, default="NULL")
    app_recent_reviews = models.TextField("app recent reviews", max_length=500, default="NULL")
    app_thumbnail = models.ImageField("app thumbnail", upload_to="steamdb/static/documents/", default="")
    app_tag = models.CharField("app Tags", max_length=500, default="NULL")
    app_release_date = models.DateTimeField("Release Date", default=now)
    app_price = models.FloatField("app price", default=0.0)
    app_news = models.TextField("app news", max_length=1000, default="NULL")
    app_info_complete = models.BooleanField("app info complete", default=False)

    def __str__(self):
        return self.app_name

    def _is_release_recently(self):
        return self.app_release_date >= now() - datetime.timedelta(days=100)
