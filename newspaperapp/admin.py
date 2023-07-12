from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscriber


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]
    filter_horizontal = ('postCategory',)  # Изменено значение поля на 'postCategory'
    list_display = ('title', 'author', 'dateCreation')


class SubscriberAdmin(admin.ModelAdmin):
    filter_horizontal = ('subscribed_categories',)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Post, PostAdmin)




