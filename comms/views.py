from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Comment
from .forms import CommentForm
from django.core import serializers


def transform_clist(clist, depth=None):
    cdict = {}
    for comment in clist:
        if depth != None and comment.depth != depth:
            continue
        cobj = {
            "obj": comment,
            "children": [],
            "more": False,
        }
        cdict[comment.pk] = cobj
    return cdict


def nested_comments(base_depth=0, root_comment_id=None):
    cqlist = Comment.objects.filter(depth__lte=base_depth + 3, depth__gte=base_depth)
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


def detailView(request):
    comments = nested_comments(base_depth=0)
    context = {"comments": comments, "is_expanded": False}
    return render(request, "comms/list.html", context)


def commentExpand(request, comment_id):
    c = Comment.objects.get(pk=comment_id)
    comments = nested_comments(base_depth=c.depth, root_comment_id=comment_id)
    context = {"comments": comments, "is_expanded": True}
    return render(request, "comms/list.html", context)


def addComment(request, comment_id):
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            if comment_id == 0:
                comment.parent_comment = None
            else:
                cparent = Comment.objects.get(pk=comment_id)
                comment.parent_comment = cparent
                comment.depth = cparent.depth + 1
            comment.save()
            return redirect("comms:detail")
    else:
        form = CommentForm()
    return render(request, "comms/add.html", {"form": form})


def searchComments(request):
    query_text = request.POST["query"]
    clist = Comment.objects.filter(comment_text__icontains=query_text)
    clist = transform_clist(clist)
    return render(request, "comms/results.html", {"comments": clist.values()})
