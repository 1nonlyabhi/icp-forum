from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from users.models import Follow
from notifications.models import Notification
from .forms import NewCommentForm

from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from users.decorators import allowed_users


decorators = [allowed_users(allowed_roles=['student', 'teacher']), login_required ]

def is_users(post_user, logged_user):
    return post_user == logged_user


PAGINATION_COUNT = 10

def welcome(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    return render(request,'blog/welcome.html')


def privacy_policy(request):
    return render(request,'blog/privacy_policy.html')

def cookies(request):
    return render(request,'blog/cookies.html')



@method_decorator(decorators, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = PAGINATION_COUNT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.values('author').annotate(author_count=Count('author')).order_by('-author_count')[:6]

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['author']).first())
        context['all_users'] = all_users

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        follows = [user]
        for obj in queryset:
            follows.append(obj.follow_user)
        return Post.objects.filter(author__in=follows).order_by('-date_posted')


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user, follow_user=visible_user).count() == 0)
        context = super().get_context_data(**kwargs)

        context['user_profile'] = visible_user
        context['can_follow'] = can_follow
        return context

    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            profile = self.visible_user()
            follows_between = Follow.objects.filter(user=request.user, follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
                        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=self.visible_user())
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        context['comments'] = comments_connected
        context['form'] = NewCommentForm(instance=self.request.user)
        return context

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        new_comment = Comment(content=request.POST.get('content'),
                              attachedurl=request.POST.get('attachedurl'),
                              author=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

        messages.success(request, 'Comment successfully submitted')

        return self.get(self, request, *args, **kwargs)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'attachedurl', 'attachedimage']
    template_name = 'blog/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add new post'
        return data


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content', 'attachedurl', 'attachedimage']
    template_name = 'blog/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_line'] = 'Edit post'
        return context


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class FollowsListView(ListView):
    model = Follow
    template_name = 'blog/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['follow'] = 'follows'
        return context


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class FollowersListView(ListView):
    model = Follow
    template_name = 'blog/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['follow'] = 'followers'
        return context


# ==================================Post Like Functionality=============================
@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)

        if not post.likes.filter(id=request.user.id).exists():
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)
        else:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

        if not post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.add(request.user)
        else:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)



# ===============================Comment Like Functionality=============================
@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)

        if not comment.likes.filter(id=request.user.id).exists():
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)
        else:
            comment.likes.remove(request.user)

        next = request.POST.get('next', 'post-detail')
        return HttpResponseRedirect(next)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)

        if not comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.add(request.user)
        else:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', 'post-detail')
        return HttpResponseRedirect(next)




def about(request):
    return render(request,'blog/about.html',)

