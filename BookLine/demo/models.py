from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    USERNAME_FIELD = 'username'

    def full_name(self):
        return self.name + ' ' + self.surname + ' ' + self.patronymic

    def __str__(self):
        return self.full_name()


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    photo_file = models.ImageField(max_length=254, upload_to=get_name_file,
                                   blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    year = models.IntegerField(verbose_name='Год издания', blank=True)
    country = models.CharField(max_length=254, verbose_name='Автор', blank=True)
    opisanie = models.CharField(max_length=254, verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False,
                                default=0.00)
                           # добавление
    # year = models.IntegerField(verbose_name='Год издания', blank=True)
    # author = models.CharField(max_length=254, verbose_name='Автор', blank=True)
    # price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False,
    #                             default=0.00)
    # izd = models.CharField(max_length=254, verbose_name='Издательство', blank=True)


    
    count = models.IntegerField(verbose_name='Количество', blank=False, default=1)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Наименование', blank=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержденный'),
        ('canceled', 'Отмененный')
    ]
    date = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOICES,
                              default='new')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    rejection_reason = models.TextField(verbose_name='Причина отказа', blank=True)
    products = models.ManyToManyField(Product, through='ItemInOrder', related_name='orders')

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def get_products(self):
        return [{'Название': i.name, 'Количество': i.count, 'Стоимость': i.price} for i in self.products.all()]

    def count_product(self):
        count_product = 0
        for iteminorder in self.iteminorder_set.all():
            count_product += iteminorder.count
        return count_product

    def __str__(self):
        return f"Дата {self.date.ctime()} | {self.user.full_name()} | Количество {self.count_product()}"


class ItemInOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=0)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False,
                                default=0.00)


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=0)

    def __str__(self):
        return self.product.name + ' - ' + str(self.count)
