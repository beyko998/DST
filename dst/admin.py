from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, ServiceOrProduct, PdfDescr, Booklet, KoshtorisProektu
from django.utils.safestring import mark_safe
admin.site.register(PdfDescr)
admin.site.register(Booklet)


class KoshtorisProektuAdmin(admin.ModelAdmin):
    list_display = ('name', 'squarem')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ServiceOrProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency_rate', 'connection_between', 'icon_tag')
    prepopulated_fields = {'slug': ('name', )}

    def icon_tag(self, obj):
        if obj.image != '':
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')
        elif obj.image == '':
            return mark_safe(f'<img src="/media/productsimage/default.png" style="max-height: 200px;">')

    icon_tag.short_description = 'Фото товара'
    icon_tag.allow_tags = True
    readonly_fields = ['icon_tag']


admin.site.register(KoshtorisProektu, KoshtorisProektuAdmin)
admin.site.register(ServiceOrProduct, ServiceOrProductAdmin)
admin.site.register(Category, CategoryAdmin)
