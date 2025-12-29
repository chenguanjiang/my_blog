from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image



# Create your models here.

class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
        

class ArticlePost(models.Model):
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='articles')

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    body = models.TextField()

    total_views = models.PositiveBigIntegerField(default=0)

    created = models.DateTimeField(default=timezone.now)

    updated = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        article = super().save(*args, **kwargs)
        
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            x, y = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.LANCZOS)
            resized_image.save(self.avatar.path)

        return article


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
