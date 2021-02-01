from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    article = models.CharField(max_length=100, verbose_name='Артикул', unique=True)
    price = models.CharField(max_length=50, verbose_name='Цена')
    url = models.URLField('URL')
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
