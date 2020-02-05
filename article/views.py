from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.urls import reverse

from account.models import MyUser
from album.models import AlbumInfo
from article.models import ArticleTag, ArticleInfo


def article(request, id, page):
    '''
    文章列表
    :param request:
    :param id:
    :param page:
    :return:
    '''
    album = AlbumInfo.objects.filter(user_id=id)
    tag = ArticleTag.objects.filter(user_id=id)
    user = MyUser.objects.filter(id=id).first()
    if not user:
        return redirect(reverse('redister'))
    # 根据博主的id查询所属博主的正文内容
    ats = ArticleInfo.objects.filter(author_id=id).order_by('-created')
    paginator = Paginator(ats, 10)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    return render(request, 'article.html', locals())

