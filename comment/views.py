from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from .forms import CommentForm
from django.urls import reverse
from article.models import ArticlePost

# Create your views here.




@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            # 处理 Profile 可能不存在的情况
            if hasattr(request.user, 'profile'):
                comment.user = request.user.profile
            else:
                from userprofile.models import Profile
                comment.user = Profile.objects.create(user=request.user)
            comment.save()
            messages.success(request, '评论已发布')
            return redirect(article.get_absolute_url())
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        return HttpResponse('请使用POST方法提交评论')
