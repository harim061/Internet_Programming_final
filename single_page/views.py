from django import db
from django.shortcuts import render
from shoppingmall_main.models import ShoppingItem,Category
from shoppingmall_main.models import Comment,ColorTag
from django.views.generic import ListView
# Create your views here.

def landing(request):
    recent_posts = ShoppingItem.objects.order_by('-pk')[:3]

    return render(request,'single_page/landing.html',{
        'recent_posts' : recent_posts,
    })


def about_me(request):
    labels = []
    data = []

    queryset = ColorTag.objects.order_by()

    for tag in queryset:
        tags = ShoppingItem.tags.through.objects.filter(colortag=tag)
        tag_count = tags.count()
        labels.append(tag.name)
        data.append(tag_count)
    return render(request,'single_page/about_me.html',{
        'labels': labels,
        'data': data,
    })

def mypage(request):
    author = request.user
    user= request.user
    comment_list = Comment.objects.filter(author=author)
    likes= ShoppingItem.like_users.through.objects.filter(user=user)
    likes_count = likes.count()
    shoppingitem = ShoppingItem.objects.filter(like_users=user)
    return render(
        request,
        'single_page/mypage.html',{
        'author':author,
        'comments' : comment_list,
        'likes':likes,
        'likes_count':likes_count,
        'shoppingitem':shoppingitem,
        }
    )

