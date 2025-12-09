from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.title


class SiteCounter(models.Model):
    total = models.PositiveBigIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '站点访问计数'
        verbose_name_plural = '站点访问计数'

    def __str__(self):
        return f"Total: {self.total}"
