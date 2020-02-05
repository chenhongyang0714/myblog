from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import render
from album.models import AlbumInfo
from article.models import ArticleTag


class MyUser(AbstractUser):
    '''
    用户(博主)信息
    '''
    name = models.CharField('姓名', max_length=50, default='匿名用户')
    introduce = models.TextField('简介', default='暂无介绍')
    company = models.CharField('公司', max_length=100, default='暂无信息')
    profession = models.CharField('职业', max_length=100, default='暂无信息')
    address = models.CharField('住址', max_length=100, default='暂无信息')
    telephone = models.CharField('电话', max_length=11, default='暂无信息')
    wx = models.CharField('微信', max_length=50, default='暂无信息')
    qq = models.CharField('QQ', max_length=50, default='暂无信息')
    wb = models.CharField('微博', max_length=100, default='暂无信息')
    photo = models.ImageField('头像', blank=True, upload_to='images/user/')  # 字符类型，存储图片路径的字符串

    # 设置返回值
    def __str__(self):
        return self.name









