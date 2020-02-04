from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse

from account.models import MyUser
from album.models import AlbumInfo
from article.models import ArticleTag
from interflow.models import Board


def board(request, id, page):
    '''
    留言板
    :param request:
    :param id:查询留言的用户id
    :param page:每页显示的留言数
    :return:
    '''
    album = AlbumInfo.objects.filter(user_id=id)
    tag = ArticleTag.objects.filter(user_id=id)
    user = MyUser.objects.filter(id=id).first()
    # 判断数据对象user是否存在
    if not user:
        return redirect(reverse('register'))
    if request.method == 'GET':
        boardList = Board.objects.filter(user_id=id).order_by('-created')  # user_id为Board的外键
        paginator = Paginator(boardList, 10)  # 分页对象
        try:
            pageInfo = paginator.page(page)
        except PageNotAnInteger:
            # 如果参数page的数据类型不是整型，就返回第一页数据
            pageInfo = paginator.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pageInfo = paginator.page(paginator.num_pages)
        return render(request, 'board.html', locals())
    # 提交留言
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        value = {
            'name': name,
            'email': email,
            'content': content,
            'user_id': id
        }
        Board.objects.create(**value)
        # 模型Board重新获取数据，将新增的数据及时显示在网页上
        kwargs = {'id': id, 'page': 1}
        return redirect(reverse('board', kwargs=kwargs))





























