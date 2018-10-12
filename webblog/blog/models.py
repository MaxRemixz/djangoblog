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
