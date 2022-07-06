from django.urls import include, path
from . import views


app_name="chat"

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("chat/<name>", views.Lobby.as_view(), name='chat'),

    # membership urls
    path("apply/<name>", views.ApplyForMemberShip.as_view(), name='apply-membership'),
    path("accept/<name>/<int:user>", views.AcceptMemberShip.as_view(), name='accept-membership'),
    path("revoke/<name>/<int:user>", views.RevokeMemberShip.as_view(), name='revoke-membership'),
    path("deny/<name>/<int:user>", views.DenyMemberShip.as_view(), name='deny-membership'),
]