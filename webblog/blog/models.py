from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import hashlib
from django.http import HttpRequest

from django.contrib.auth.models import UserManager


class User(AbstractUser):

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )

    adder = models.CharField(max_length=50, blank=True, null=True, verbose_name='地址')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号码')
    birthday = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=gender_choices, default=1)
    avatar_hash = models.CharField(max_length=32, blank=True, null=True)
    #objects = models.Manager()
    objects = UserManager()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()


    # def change_email(self):
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=256, default='identicon', rating='g'):
        if HttpRequest.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    def index_gravatar(self, size=40, default='identicon', rating='g'):
        if HttpRequest.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    # 关注相关的方法
    def follow(self, user):
        if not self.is_following(user):
            f = FriendShip(follower=self, followed=user)
            f.save()

    def unfollow(self, user):
        try:
            f = FriendShip.objects.get(follower=self, followed=user)
        except:
            return None
        if f:
            f.delete()

    def is_following(self, user):
        if user.id is None:
            return False
        try:
            f = FriendShip.objects.get(follower=self, followed=user)
        except:
            return False
        return True

    def is_followed_by(self, user):
        if user.id is None:
            return False
        try:
            f = FriendShip.objects.get(follower=self, followed=user)
        except:
            return False
        return True

    # 获取所关注用户的文章
    @property
    def followed_posts(self):
        user = FriendShip.objects.filter(follower=self).values_list('followed_id')
        return Blog_Articles.objects.filter(author_id__in=user)


class Blog_Articles(models.Model):
    title = models.CharField(max_length=80, blank=False, verbose_name='标题')
    body = models.TextField(blank=False, verbose_name='内容')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    objects = models.Manager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class FriendShip(models.Model):
    followed = models.ForeignKey(User, related_name='followed', verbose_name='粉丝', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower', verbose_name='关注', on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    objects = models.Manager()


class Comment(models.Model):
    body = models.CharField(max_length=500, verbose_name='内容')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='评论时间')
    disabled = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', related_name='author_comments')
    post = models.ForeignKey(Blog_Articles, on_delete=models.CASCADE, verbose_name='文章', related_name='post_comments')
    objects = models.Manager()

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body
