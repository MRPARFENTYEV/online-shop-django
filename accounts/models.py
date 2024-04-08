from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from shop.models import Product

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(Product, blank=True, related_name='лайки')
    # set a manager role for shop manager to access orders and products
    is_manager = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)
    store_name = models.CharField(max_length=50, verbose_name='СлагМагазина', default='No_store')


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    search_fields =['full_name']
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'





    def __str__(self):
        return self.email



    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_likes_count(self):
        return self.likes.count()



class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts', blank=True, null=True,
                             on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True,null=True,)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True, null=True,)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True, null=True,)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True,null=True,)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.house} {self.apartment} {self.phone} {self.user}'

