from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import TreeRelatedFieldListFilter
from .models import Category, ServiceOrProduct, PdfDescr, Booklet, KoshtorisProektu
from django.utils.safestring import mark_safe

admin.site.register(Booklet)


class PdfDescrAdmin(admin.ModelAdmin):
    list_display = ('name', 'connection_between',)
    search_fields = ('connection_between__name',)


class KoshtorisProektuAdmin(admin.ModelAdmin):
    list_display = ('name', 'squarem')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(DjangoMpttAdmin):
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )
    prepopulated_fields = {'slug': ('name',)}


class ServiceOrProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'currency_rate', 'connection_between', 'icon_tag', 'sale')
    prepopulated_fields = {'slug': ('name', )}
    list_filter = ('connection_between', 'sale')
    search_fields = ('name', 'description', 'id', 'slug', 'connection_between__name')
    list_editable = ('price', 'currency_rate', 'connection_between', 'sale',)

    def icon_tag(self, obj):
        if obj.image != '':
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 50px;">')
        elif obj.image == '':
            return mark_safe(f'<img src="/media/productsimage/default.png" style="max-height: 50px;">')

    icon_tag.short_description = 'Фото товара'
    icon_tag.allow_tags = True
    readonly_fields = ['icon_tag']


admin.site.register(KoshtorisProektu, KoshtorisProektuAdmin)
admin.site.register(ServiceOrProduct, ServiceOrProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PdfDescr, PdfDescrAdmin)
