from django.db import models
from django.contrib.auth import get_user_model


class AccessTokenModel(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    access_token = models.CharField(max_length=256, null=False, blank=False)
    access_token_secret = models.CharField(max_length=256, null=False, blank=False)
