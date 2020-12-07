import datetime
from django.db import models
from django.utils import timezone


class Post(models.Model):
    post_text = models.CharField(max_length=200)
    published = models.DateTimeField("date published", auto_now=True)

    def __str__(self):
        return self.post_text


class Comment(models.Model):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )

    comment_text = models.CharField(max_length=200)
    depth = models.IntegerField(default=0)
    published = models.DateTimeField("date published", auto_now=True)

    def __str__(self):
        return self.comment_text
