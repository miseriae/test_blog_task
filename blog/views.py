from django.shortcuts import render, get_object_or_404
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
    page = request.GET.get('page', 1)
    paginator = Paginator(allcomments, 6)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect(post.slug)
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': user_comment,
        'comments': comments,
        'comment_form': comment_form,
        'allcomments': allcomments
    }
    return render(request, 'post_detail.html', context=context)


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
