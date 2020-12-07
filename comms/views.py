from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from .forms import CommentForm


def transform_clist(clist, depth):
    cdict = {}
    for comment in clist:
        if comment.depth != depth:
            continue
        cobj = {
            "obj": comment,
            "children": [],
            "more": False,
        }
        cdict[comment.pk] = cobj
    return cdict


def nested_comments(post_id, base_depth=0, root_comment_id=None):
    p = Post.objects.get(pk=post_id)
    cqlist = p.comment_set.filter(depth__lte=base_depth + 3, depth__gte=base_depth)
    c0 = transform_clist(cqlist, base_depth + 0)
    c1 = transform_clist(cqlist, base_depth + 1)
    c2 = transform_clist(cqlist, base_depth + 2)
    c3 = transform_clist(cqlist, base_depth + 3)
    for c in c3:
        cparent = c3[c]["obj"].parent_comment.pk
        if cparent in c2:
            c2[cparent]["more"] = True
    for c in c2:
        cparent = c2[c]["obj"].parent_comment.pk
        if cparent in c1:
            c1[cparent]["more"] = True
            c1[cparent]["children"].append(c2[c])
    for c in c1:
        cparent = c1[c]["obj"].parent_comment.pk
        if cparent in c0:
            c0[cparent]["more"] = True
            c0[cparent]["children"].append(c1[c])
    if root_comment_id != None:
        if root_comment_id in c0:
            return [c0[root_comment_id]]
        else:
            return []
    return list(c0.values())


def postDetail(request, post_id):
    comments = nested_comments(post_id, base_depth=0)
    context = {"post_id": post_id, "comments": comments, "is_expanded": False}
    return render(request, "comms/post.html", context)


def commentExpand(request, post_id, comment_id):
    c = Comment.objects.get(pk=comment_id)
    comments = nested_comments(post_id, base_depth=c.depth, root_comment_id=comment_id)
    context = {"post_id": post_id, "comments": comments, "is_expanded": True}
    return render(request, "comms/post.html", context)


def addComment(request, post_id, comment_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if comment_id == 0:
                comment.parent_comment = None
            else:
                cparent = Comment.objects.get(pk=comment_id)
                comment.parent_comment = cparent
                comment.depth = cparent.depth + 1
            comment.parent_post = Post.objects.get(pk=post_id)
            comment.save()
            return redirect("comms:detail", post_id=post_id)
    else:
        form = CommentForm()
    return render(request, "comms/add.html", {"form": form})
