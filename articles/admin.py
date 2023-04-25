from django.contrib import admin
from .models import Articles

# Register your models here.

admin.site.register(Articles)

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'author', 'like_count']}),
        ('Context', {'fields': ['text']})
    ]
    readonly_fields = ['like_count', 'is_popular']
    search_fields = ['title', 'author', 'text']
    list_display = ['title', 'author', 'like_count', 'is_popular']
    list_filter = ['title', 'author']