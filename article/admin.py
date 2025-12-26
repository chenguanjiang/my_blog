from django.contrib import admin

from article.models import ArticlePost, ArticleColumn

# Register your models here.

admin.site.register(ArticlePost)
admin.site.register(ArticleColumn)