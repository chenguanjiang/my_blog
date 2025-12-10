import os
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import F
from django.conf import settings

from article.models import ArticlePost, SiteCounter


# Create your views here.

#文章列表
#文章列表
def article_list(request):
    #取出所有博客文章
    articles = ArticlePost.objects.all()
    #需要传递给模板template的对象
    context = {
        'articles': articles
    }
    return render(request, 'article/list.html', context)

#文章详情
def article_detail(request, id):
    #取出相应的文章
    article = ArticlePost.objects.get(id=id)
    #需要传递给模板的对象
    context = {
        'article': article
    }
    return render(request, 'article/detail.html', context)


def home(request):
    counter, _ = SiteCounter.objects.get_or_create(pk=1, defaults={'total': 0})
    SiteCounter.objects.filter(pk=counter.pk).update(total=F('total') + 1)
    counter.refresh_from_db()
    base_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'newboy')
    names = []
    if os.path.isdir(base_dir):
        for f in os.listdir(base_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                names.append(f)
    newboy_images = [{'src': f"/static/img/newboy/{name}", 'title': os.path.splitext(name)[0]} for name in sorted(names)]
    context = {
        'visits_total': counter.total,
        'newboy_images': newboy_images
    }
    return render(request, 'index.html', context)
