# Generated by Django 3.2 on 2022-12-19 00:10

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingmall_main', '0006_alter_shoppingitem_like_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingitem',
            name='information',
            field=markdownx.models.MarkdownxField(),
        ),
    ]