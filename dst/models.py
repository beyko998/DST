from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse


class Category(MPTTModel):

    name = models.CharField(max_length=200, verbose_name='Назва', help_text="Категорія", db_index=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                          db_index=True, verbose_name='Головна категорія')
    slug = models.SlugField(max_length=200, verbose_name='URL',
                            help_text="Коротка назва для url", unique=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def get_absolute_url(self):
        return reverse('product_by_category', args=[str(self.slug)])

    def __str__(self):
        return self.name


class ServiceOrProduct(models.Model):

    name = models.CharField(max_length=200, verbose_name='Назва', help_text="Назва товару чи послуги", db_index=True)
    image = models.ImageField(upload_to='productsimage/%Y/%m/%d/', verbose_name='Фото',  blank=True, help_text="фото",
                              null=True)
    description = models.TextField(help_text="Опис товару чи послуги", verbose_name='Опис')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна', help_text="Ціна")
    UAN = 'UAN'
    EUR = 'EUR'
    USD = 'USD'
    currency = [
        (UAN, 'UAN'),
        (EUR, 'EUR'),
        (USD, 'USD'),
    ]
    currency_rate = models.CharField(max_length=3, choices=currency, default='EUR', verbose_name='Валюта',
                                     help_text="Виберіть валюту")
    slug = models.SlugField(max_length=200, verbose_name='URL',
                            help_text="Коротка назва для url", unique=True, blank=True)
    sale = models.BooleanField(default=False, verbose_name='Знижка')
    connection_between = TreeForeignKey(Category, related_name='ServiceOrProducts', verbose_name="Группа товару",
                                        on_delete=models.CASCADE,)

    class Meta:
        verbose_name = 'Товар/Послуга'
        verbose_name_plural = 'Товари/Послуги'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('name', args=[str(self.slug)])


class PdfDescr(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва",
                            help_text="Назва файлу", db_index=True, default='.pdf')
    connection_between = models.OneToOneField(ServiceOrProduct, verbose_name="Зв'язок з товаром",
                                              on_delete=models.CASCADE, help_text="Зв'язати з товаром")
    pdfvalue = models.FileField(upload_to='pdfdescr/%Y/%m/%d/', verbose_name=".PDF файл", blank=True, help_text=".pdf")

    class Meta:
        verbose_name = '.pdf файл продукту'
        verbose_name_plural = '.pdf файли продуктів'

    def __str__(self):
        return self.name


class Booklet(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва",
                            help_text="Назва буклету", db_index=True)
    pdfvalue = models.FileField(upload_to='booklets/%Y/%m/%d/', default="", verbose_name=".PDF файл", blank=True,
                                help_text=".pdf")

    class Meta:
        verbose_name = 'Буклет'
        verbose_name_plural = 'Буклети'

    def __str__(self):
        return self.name


class KoshtorisProektu(models.Model):

    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    name = models.CharField(max_length=200, verbose_name="Назва",
                            help_text="Назва проекту", db_index=True)
    proj_square = models.CharField(max_length=200, verbose_name="Площа об'єкту",
                            help_text="Площа м2")
    location = models.CharField(max_length=200, verbose_name="Місце знаходження об'єкту",
                            help_text="Де знаходиться об'єкт")
    customer = models.CharField(max_length=200, verbose_name="Замовник",
                            help_text="ПІБ замовника")
    company_descr = models.CharField(max_length=200, verbose_name="Опис компанії",
                            help_text="Опис компанії", blank=True)
    creators = models.CharField(max_length=200, verbose_name="Засновники компанії",
                            help_text="ПІБ Засновників", blank=True)
    performer = models.CharField(max_length=200, verbose_name="Виконавець",
                            help_text="ПІБ виконавця")
    notation = models.TextField(verbose_name="Примітки",
                            help_text="Примітки", blank=True)
    title_pdf = models.FileField(upload_to='static/', default="", verbose_name="Титулка", blank=True,
                                help_text=".pdf")

    class Meta:
        verbose_name = 'Шаблон КП'
        verbose_name_plural = 'Шаблони КП'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def squarem(self):
        return self.proj_square + ' м\u00b2 '

    squarem.short_description = "Площа об'єкту"

    def get_absolute_url(self):
        return reverse('product', args=[str(self.slug)])
