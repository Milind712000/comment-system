from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = "comms"
urlpatterns = [
    path("", views.detailView, name="detail"),
    path(
        "comment/<int:comment_id>",
        views.commentExpand,
        name="commentExpand",
    ),
    path(
        "add/comment/<int:comment_id>",
        views.addComment,
        name="addComment",
    ),
    path("search/", views.searchComments, name="search"),
]
