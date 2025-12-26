import os
from django.http import HttpResponse
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Count
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlparse
from django.db.models import Q
from comment.models import Comment



from article.forms import ArticlePostForm
from article.models import ArticlePost, SiteCounter, ArticleColumn


# Create your views here.


def article_list(request):
    search = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'created')
    if search:
        articles = ArticlePost.objects.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        ).annotate(comment_count=Count('comments')).order_by(f'-{order}')
    else:
        articles = ArticlePost.objects.all().annotate(comment_count=Count('comments')).order_by(f'-{order}')
    paginator = Paginator(articles, 6)
    page = request.GET.get('page', 1)
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'order': order,
        'search': search
    }
    return render(request, 'article/list.html', context)

#文章详情
def article_detail(request, id):
    article = get_object_or_404(ArticlePost, id=id)
    comments = Comment.objects.filter(article=article)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    article.body = markdown.markdown(article.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
    ])
    ref = request.META.get('HTTP_REFERER') or ''
    back_list_url = reverse('article:article_list')
    if ref:
        p = urlparse(ref)
        if 'article-list' in p.path:
            back_list_url = ref
    context = {
        'article': article,
        'back_list_url': back_list_url,
        'comments': comments,
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


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            messages.success(request, '文章已发布')
            return redirect('article:article_list')
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all().order_by('-created')
        context = { 'article_post_form': article_post_form, 'columns': columns }
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    if request.method == 'POST':
        article = get_object_or_404(ArticlePost, id=id)
        if request.user.is_authenticated and request.user == article.author:
            article.delete()
            messages.success(request, '文章已删除')
            return redirect('article:article_list')
        else:
            return HttpResponse("您没有权限删除该文章")
    else:
        return HttpResponse("仅允许POST请求")


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        if request.user.is_authenticated and request.user == article.author:
            article_post_form = ArticlePostForm(data=request.POST)
            if article_post_form.is_valid():
                article.title = request.POST['title']
                article.body = request.POST['body']
                col_id = request.POST.get('column')
                if col_id:
                    try:
                        article.column = ArticleColumn.objects.get(id=col_id)
                    except ArticleColumn.DoesNotExist:
                        article.column = None
                else:
                    article.column = None
                article.save()
                messages.success(request, '文章已更新')
                return redirect('article:article_detail', id=id)
            else:
                return HttpResponse("表单内容有误，请重新填写")
        else:
            return HttpResponse("您没有权限更新该文章")
    else:
        article_post_form = ArticlePostForm()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': ArticleColumn.objects.all().order_by('-created'),
        }
        return render(request, 'article/update.html', context)
