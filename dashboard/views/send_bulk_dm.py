from re import A
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from ..twitter_oauth import TwitterAuthAPI
from ..twitter_oauth.contrib import TwitterActions
from ..forms import DMForm
from ..models import AccessTokenModel
import logging

logger = logging.getLogger(__name__)

@login_required
def send_bulk_dm_view(request):
    user = get_user(request)
    if request.POST:
        form = DMForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data.get("text")
            try:
                access_keys = AccessTokenModel.objects.get(user=user)
                twitter = TwitterAuthAPI(
                        access_keys.access_token,
                        access_keys.access_token_secret
                    )
                twitter_api = twitter.API
                cursor = TwitterActions(twitter_api)
                followers = cursor.get_followers()
                cursor.send_bulk_direct_message(followers, msg)
            except AccessTokenModel.DoesNotExist as e:
                logger.exception(e)
    context = {"form": DMForm(), "user": get_user(request)}
    return render(request, "dashboard/bulk_dm.html", context=context)
