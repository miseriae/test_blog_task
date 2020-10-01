from django import forms

from mptt.forms import TreeNodeChoiceField
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'body', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control' }),
            'slug': forms.TextInput(attrs={'class': 'form-control' }),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False


    class Meta:
        model = Comment
        fields = ('content', 'parent')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
