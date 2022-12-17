from django.shortcuts import render
from shoppingmall_main.models import ShoppingItem
from shoppingmall_main.models import Comment
from django.views.generic import ListView
# Create your views here.

def landing(request):
    recent_posts = ShoppingItem.objects.order_by('-pk')[:3]
    return render(request,'single_page/landing.html',{
        'recent_posts' : recent_posts,
    })

def about_me(request):
    return render(request,'single_page/about_me.html')

def mypage(request):
    author = request.user

    comment_list = Comment.objects.filter(author=author)
    likes_count = ShoppingItem.like_users.through.objects.count()

    return render(
        request,
        'single_page/mypage.html',{
        'author':author,
        'comments' : comment_list,
        'likes_count':likes_count,
        }
    )

