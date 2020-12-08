from django import forms

from .models import Comment

# Django Form for creating a Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_text", "comment_media")
