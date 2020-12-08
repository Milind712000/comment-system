import datetime
from django.db import models
from django.utils import timezone

# Comment Table Schema
class Comment(models.Model):
    # Self refrencing ForeignKey (One to Many Relationship)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )

    # Comment Contents (Text and Image)
    comment_text = models.CharField(max_length=200)
    comment_media = models.ImageField(upload_to="imgs/", blank=True, null=True)

    # Integer Field to store depth of nesting
    depth = models.IntegerField(default=0)
    # Automatically Recorded Field to save time of storage
    published = models.DateTimeField("date published", auto_now=True)

    def __str__(self):
        return self.comment_text
