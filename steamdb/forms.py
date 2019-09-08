from django import forms

from .models import SteamDB


class AppEditForm(forms.ModelForm):
    class Meta:
        model = SteamDB
        fields = (
            'app_desc',
            'app_tag',
            'app_publisher',
            'app_developer',
            'app_history_reviews',
            'app_recent_reviews',
            'app_release_date',
            'app_price',
            'app_news',
            'app_thumbnail',
        )
