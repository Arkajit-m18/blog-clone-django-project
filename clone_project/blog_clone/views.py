from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from .models import Post, Comment
from .forms import UserForm, UserProfileInfoForm, PostForm, CommentForm

# Create your views here.

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class AboutView(TemplateView):
    template_name = 'about.html'

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    redirect_field_name = 'blog_clone/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'blog_clone/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    success_url = reverse_lazy('post_list')
    model = Post

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Post
    redirect_field_name = 'blog_clone/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect('post_detail', pk = post.pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
        else:
            print(form.errors)
    else:
        form = CommentForm()
    return render(request, 'blog_clone/comment_form.html', {'form': form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    form = CommentForm(instance = comment)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.author = form.cleaned_data['author']
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('post_detail', pk = comment.post.pk)
        else:
            print(form.errors)
    return render(request, 'blog_clone/comment_form.html', {'form': form})

@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk = post_pk)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'auth/registration.html', {'registered': registered, 'user_form': user_form, 'profile_form': profile_form, 'site_path': 'register'})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('post_list'))
            else:
                return HttpResponse('User not active')
        else:
            return HttpResponse('Invalid login credentials')
    else:
        return render(request, 'auth/login.html', {'site_path': 'login'})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))