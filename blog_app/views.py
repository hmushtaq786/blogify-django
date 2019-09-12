from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from blog_app.models import Post, Comment
from django.urls import reverse_lazy
from blog_app.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # lte = less than equal to. get_queryset acts like sql query. dash (-) with published_date means order in descending order
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):

    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'

    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):

    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'

    form_class = PostForm

    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = 'blog_app/post_list.html'

    model = Post

    def get_queryset(self):
        # lte = less than equal to. get_queryset acts like sql query. dash (-) with published_date means order in descending order
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')


@login_required
def add_comments_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    form = CommentForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

        else:
            form = CommentForm()

    return render(request, 'blog_app/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()

    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
