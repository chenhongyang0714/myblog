from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, redirect
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.urls import reverse

from account.models import MyUser
from album.models import AlbumInfo
from article.models import ArticleTag, ArticleInfo, Comment


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


def detail(request, id, aId):
    '''
    文章正文内容
    :param request:
    :param id: 模型MyUser的主键id
    :param aId: 模型ArticleInfo的主键id
    :return:
    '''
    album = AlbumInfo.objects.filter(user_id=id)
    tag = ArticleTag.objects.filter(user_id=id)
    user = MyUser.objects.filter(id=id).first()
    if request.method == 'GET':
        ats = ArticleInfo.objects.filter(id=aId).first()
        # 每篇文章的所有分类标签，atags为可迭代对象
        atags = ArticleInfo.objects.get(id=aId).article_tag.all()
        # 每篇文章的所有评论信息
        cms = Comment.objects.filter(article_id=aId).order_by('-created')

        # 添加阅读量(每个用户仅能增加一次)
        if not request.session.get('reading' + str(id) + str(aId)):
            reading = ArticleInfo.objects.filter(id=aId)
            # 阅读量+1
            reading.update(reading=F('reading') + 1)
            # 记录 "增加阅读量记录" 到session
            request.session['reading' + str(id) + str(aId)] = True
        return render(request, 'detail.html', locals())
    # POST 提交文章评论内容
    else:
        commentator = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        value = {
            'commentator': commentator,
            'content': content,
            'article_id': aId
        }
        Comment.objects.create(**value)

        kwargs = {'id': id, 'aId': aId}
        return redirect(reverse('detail', kwargs=kwargs))





























