from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    body = models.TextField()

    total_views = models.PositiveBigIntegerField(default=0)

    created = models.DateTimeField(default=timezone.now)

    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', kwargs={'id': self.id})


class SiteCounter(models.Model):
    total = models.PositiveBigIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '站点访问计数'
        verbose_name_plural = '站点访问计数'

    def __str__(self):
        return f"Total: {self.total}"
