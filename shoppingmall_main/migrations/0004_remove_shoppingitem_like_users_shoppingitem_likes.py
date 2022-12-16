# Generated by Django 4.1.4 on 2022-12-17 02:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shoppingmall_main', '0003_rename_like_shoppingitem_like_users_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingitem',
            name='like_users',
        ),
        migrations.AddField(
            model_name='shoppingitem',
            name='likes',
            field=models.ManyToManyField(related_name='likes_item', to=settings.AUTH_USER_MODEL),
        ),
    ]