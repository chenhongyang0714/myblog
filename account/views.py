from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

from account.models import MyUser
from album.models import AlbumInfo
from article.models import ArticleTag


def register(request):
    '''
    用户注册
    :param request:
    :return:
    '''
    title = '注册博客'
    pageTitle = '用户注册'
    confirmPassword = True
    button = '注册'
    urlText = '用户登录'
    urlName = 'userLogin'
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        cp = request.POST.get('cp', '')
        if MyUser.objects.filter(username=u):
            tips = '用户已存在'
        elif cp != p:
            tips = '两次密码输入不一致！'
        else:  # 创建用户
            d = {
                'username': u, 'password': p,
                'is_superuser': 1, 'is_staff': 1
            }
            user = MyUser.objects.create_user(**d)
            user.save()
            tips = '注册成功，请登录'
            logout(request)
            return redirect(reverse('userLogin'))
    return render(request, 'user.html', locals())


def userLogin(request):
    '''
    用户登陆
    :param request:
    :return:
    '''
    title = '登录博客'
    pageTitle = '用户登录'
    button = '登录'
    urlText = '用户注册'
    urlName = 'register'
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        if MyUser.objects.filter(username=u):
            user = authenticate(username=u, password=p)  # 对用户信息进行验证
            if user:
                if user.is_active:
                    login(request, user)
                # 登录成功后，直接重定向到  "文章列表"
                kwargs = {'id': request.user.id, 'page': 1}
                return redirect(reverse('article', kwargs=kwargs))
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    else:  # GET 已经登陆的情况下 再进登录的路由自动跳转到文章首页
        if request.user.username:
            kwargs = {'id': request.user.id, 'page': 1}
            return redirect(reverse('article', kwargs=kwargs))
    return render(request, 'user.html', locals())


def about(request, id):
    '''
    博主资料
    :param request:
    :param id: 某一位博主的博客账号
    :return:
    '''
    album = AlbumInfo.objects.filter(user_id=id)  # 数据表中的外键关联user_id
    tag = ArticleTag.objects.filter(user_id=id)
    # .first() 把QuerySet对象转化为字典对象，方便取属性值
    user = MyUser.objects.filter(id=id).first()  # 直接就是用户的id
    return render(request, 'about.html', locals())




















