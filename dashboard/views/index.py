from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from ..models import AccessTokenModel
from ..twitter_oauth import TwitterAuthAPI
import logging

logger = logging.getLogger(__name__)


@login_required()
def profile_view(request):
    user = get_user(request)
    access_keys = None
    try:
        access_keys = AccessTokenModel.objects.get(user=user)
    except AccessTokenModel.DoesNotExist:
        access_keys = None
    if not access_keys and request.GET:
        if request.GET.get("oauth_token") and request.GET.get("oauth_verifier"):
            oauth_token = request.GET.get("oauth_token")
            oauth_verifier = request.GET.get("oauth_verifier")
            twitter = TwitterAuthAPI()
            access_keys = twitter.authenticate(oauth_token, oauth_verifier)
            if access_keys:
                access_tokens = AccessTokenModel()
                access_tokens.access_token = access_keys[0]
                access_tokens.access_token_secret = access_keys[1]
                access_tokens.user = user
                access_tokens.save()
            else:
                logger.error("not access_keys")
        context = {"user": user}
        return render(request, "dashboard/profile.html", context=context)
    elif not access_keys:
        twitter = TwitterAuthAPI()
        auth_url = twitter.authorization_url
        context = {"user": user, "auth_url": auth_url}
        return render(request, "dashboard/profile.html", context=context)
    else:
        context = {"user": user}
        return render(request, "dashboard/profile.html", context=context)
