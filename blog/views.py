from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment
from .forms import CommentForm, PostForm


def home(request):
    all_posts = Post.objects.all()
    return render(request, 'home.html', {'posts': all_posts})


@login_required
def post_detail(request, post):
    post = get_object_or_404(Post, slug=post)
    allcomments = post.comments.all()
    comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
        'allcomments': allcomments
    }
    return render(request, 'post_detail.html', context=context)


def addcomment(request):
    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.user = request.user
                user_comment.save()
                result = comment_form.cleaned_data.get('content')
                user = request.user.username
                return JsonResponse({'result': result, 'user': user})


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
