from django.contrib import admin
from .models import Category, Article


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'views', 'created_at', 'updated_at', 'publish')
    list_display_links = ('title',)
    list_editable = ('publish',)
    readonly_fields = ('views',)
    list_filter = ('title', 'category', 'created_at')


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
