from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json


def index(request):
    if request.method == 'POST':
        poster_username = request.user
        content = request.POST['post_content']

        new_post = Post.objects.create(poster_username = poster_username, content = content)
        new_post.save()
    
    all_posts = Post.objects.all()
    all_posts = all_posts.order_by("-created_at").all()
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_title": "All Posts",
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    
    not_owner = profile_user != request.user
    following = False
    if not_owner:
        following = request.user in profile_user.followers.all()
            
    profile_posts = Post.objects.filter(poster_username_id=user_id)
    profile_posts = profile_posts.order_by("-created_at").all()
    paginator = Paginator(profile_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html",{
        "profile_user":profile_user,
        "follow_button": not_owner,
        "following": following,
        "page_obj": page_obj
    })

@login_required
@csrf_exempt
def follow_unfollow_user(request, user_id):
    current_user = request.user
    target_user = User.objects.get(pk=user_id)
    
    if current_user == target_user:
        return JsonResponse({'error': 'user should not be able to follow themselves.'}, status=400)
    
    if current_user in target_user.followers.all():
        target_user.followers.remove(current_user)
        is_following = False
    else:
        target_user.followers.add(current_user)
        is_following = True
    
    return JsonResponse({'is_following': is_following})

@login_required
def following(request):
    user = request.user
    following_users = user.following.all()
    following_posts = Post.objects.filter(poster_username__in=following_users)
    following_posts = following_posts.order_by("-created_at").all()

    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_title": "Following",
        "page_obj": page_obj
    })

@csrf_exempt
@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(poster_username = request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        new_post_content = json.loads(request.body)
        if new_post_content.get("content") is not None:
            post.content = new_post_content["content"]
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

def like_unlike(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if post.has_liked(request.user):
        post.unlike(request.user)
        likes_count = post.count_likes()
        return JsonResponse({"likes_count": likes_count})
    else:
        post.like(request.user)
        likes_count = post.count_likes()
        return JsonResponse({"likes_count": likes_count})