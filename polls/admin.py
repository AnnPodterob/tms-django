from django.contrib import admin

# Register your models here.

from .models import Question, Choice

# admin.site.register(Question)
# admin.site.register(Choice)

class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ['votes']
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['was_published_recently']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date', 'was_published_recently']})
    ]
    search_fields = ['question_text']
    list_filter = ['pub_date']
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ['votes']
    search_fields = ['choice_text', 'question.question_text']
    list_display = ['choice_text', 'votes', 'get_question_text']
