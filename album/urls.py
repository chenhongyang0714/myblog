from django.urls import path
from .views import *

urlpatterns = [
    # 图片墙 (MyUser的主键id/ 图片分页后的某一页页数)
    path('<int:id>/<int:page>.html', album, name='album'),
]
