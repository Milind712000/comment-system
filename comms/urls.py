from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = "comms"
# Route Definitions Summary
# GET / 
#     see all comments
# GET /comment/:id
#     see expanded view of a paticular comment
# GET add/comment/:id
#     get form to reply to parent comment with pk = (id)
# POST add/comment/:id
#     post new root comment or reply to parent comment pk = id, if id = 0 then it is a root comment
# POST search/
#     post search query to search comments by text, redirects to results

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
