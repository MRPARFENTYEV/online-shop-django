from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
import codecs
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='title')
    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        return super().save(*args, **kwargs) # Эта функция сохраняет модель в базе данных.
                                            # Она вызывает метод save() родительского класса (в данном случае Category),
                                            # передавая ему все аргументы, полученные при
                                            # вызове функции (в данном случае self, *args и **kwargs).


class Store(models.Model):
    title = models.CharField(max_length=25)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store')
    image = models.ImageField(upload_to='products')
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-date_created',)


    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})# функция reverse конструирует путь -
                                                                        #  reverse('articlrs_2003') -> 'articles/2003'
                                                                        #  reverse('articles_year_month', args = [2011,3]) ->'articles/2011/3
                                                                        #  reverse('articles_year_month', kwargs = ['year':2011,'manth':3]) -> 'articles/2011/3'
    def save(self, *args, **kwargs): #создаю слаги
        self.slug = slugify(str(self.title) +'_'+ str(self.store))
        return super().save(*args, **kwargs)



