from django.shortcuts import render
from shoppingmall_main.models import ShoppingItem
from shoppingmall_main.models import Comment
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

    return render(
        request,
        'single_page/mypage.html',{
        'comments' : comment_list,
        }
    )
