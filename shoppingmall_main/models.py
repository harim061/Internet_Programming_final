from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django import forms

import os
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=30, unique=True) # 제조사명
    address = models.CharField(max_length=30) # 제조사 주소
    tel = models.CharField(max_length=15) # 제조사 연락처
    email = models.EmailField() # 제조사 이메일

    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True,null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shoppingmall_main/m_company/{self.slug}'

    class Meta:
        verbose_name_plural = 'Companies'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shoppingmall_main/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

class ColorTag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200,unique=True,allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shoppingmall_main/tag/{self.slug}'

class ShoppingItem(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50) # 상품 이름
    information = MarkdownxField() # 상품 설명
    price = models.IntegerField() # 가격
    like_users = models.ManyToManyField(User,related_name='like_shopping',blank=True)
    head_image = models.ImageField(upload_to='shoppingmall_main/images/%Y/%m/%d/', blank=True) # 상품 이미지
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    m_company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL) # 제조사
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE) # 카테고리
    product_number = models.IntegerField() # 그 외 상품번호
    tags = models.ManyToManyField(ColorTag,blank=True) # 다대다 관계

    def __str__(self):
        return f'{self.title} by {self.m_company}'

    def get_absolute_url(self):
        return f'/shoppingmall_main/{self.pk}/'
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

    def get_content_markdown(self):
        return markdown(self.information)

class SubComment(models.Model):

    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='subcomment')
    content = models.TextField(null=False)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    shoppingitem = models.ForeignKey(ShoppingItem, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.shoppingitem.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

class ReComment(models.Model):
    post = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content