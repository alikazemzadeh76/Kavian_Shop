from django.contrib import admin
from . import models

class InformationsAdmin(admin.StackedInline):
    model = models.Information

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shamsidate", "show_image")
    inlines = (InformationsAdmin,)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'shamsidate', 'text', 'status')


admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Like)


