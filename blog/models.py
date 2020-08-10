from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):

    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11,null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.png')
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    blog = models.ForeignKey('Blog', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.username

class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="个人博客标题")
    site_name = models.CharField(max_length=64, verbose_name="站点名称")
    theme = models.CharField(max_length=32, verbose_name="博客主题")

    def __str__(self):

        return self.title


class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="分类标题")
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)

    def __str__(self):

        return self.title

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="标签名称")
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="文章标题")
    desc = models.CharField(max_length=64, verbose_name="文章描述")
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey('Category',null=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article','tag')
    )

    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag')
        ]

    def __str__(self):
        v = f"{self.article.title}---{self.tag.title}"
        return v


class ArticleUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True,on_delete=models.CASCADE)
    article = models.ForeignKey('Article', null=True,on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user')
        ]


class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    parent_comment= models.ForeignKey("self",null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.content





