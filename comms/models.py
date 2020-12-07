import datetime
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )

    comment_text = models.CharField(max_length=200)
    comment_media = models.ImageField(upload_to="imgs/", blank=True, null=True)
    depth = models.IntegerField(default=0)
    published = models.DateTimeField("date published", auto_now=True)

    def __str__(self):
        return self.comment_text
