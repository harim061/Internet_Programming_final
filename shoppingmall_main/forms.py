from .models import Comment,ReComment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class SubCommentForm(forms.ModelForm):
    class Meta:
        model = ReComment
        fields = ('content', )