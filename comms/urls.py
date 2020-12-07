from django.urls import path
from . import views

app_name = "comms"
urlpatterns = [
    path(
        "post/<int:post_id>/comment/<int:comment_id>",
        views.commentExpand,
        name="commentExpand",
    ),
    path("post/<int:post_id>", views.postDetail, name="detail"),
    path(
        "add/post/<int:post_id>/comment/<int:comment_id>",
        views.addComment,
        name="addComment",
    ),
    path("search/", views.searchComments, name="search"),
]
