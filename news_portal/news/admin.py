from django.contrib import admin
from .models import (Author, Category, Post, PostCategory,
                     Comment, Subscriber)


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]
    list_filter = ('post', 'category')
    search_fields = ('post', 'category__name')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment)
admin.site.register(Subscriber)
