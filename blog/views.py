from django.shortcuts import render, get_object_or_404
from .models import Post
from .tistory import fetch_tistory_posts

def post_list(request):
    tistory_posts = fetch_tistory_posts(limit=4)
    return render(request, "blog/post_list.html", {"tistory_posts": tistory_posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})
