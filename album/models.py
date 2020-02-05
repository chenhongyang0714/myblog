from django.db import models
from account.models import MyUser


class AlbumInfo(models.Model):
    '''
    存储图片墙的图片信息
    '''
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户')  # one to more

    title = models.CharField('标题', max_length=50, blank=True)
    introduce = models.CharField('描述', max_length=200, blank=True)
    photo = models.ImageField('图片', blank=True, upload_to='images/album/')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '图片墙管理'
        verbose_name_plural = '图片墙管理'
