from django.urls import path
from .views import profile_view, send_bulk_dm_view

urlpatterns = [
    path("", profile_view, name="dashboard"),
    path("bulk_dm/", send_bulk_dm_view, name="bulk_dm"),
]
