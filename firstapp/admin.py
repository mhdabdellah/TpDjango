from django.contrib import admin
from . import models

# Register your models here.

# admin.site.register(models.Question)
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

# admin.site.register(models.Question, QuestionAdmin)

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('question_text', 'pub_date')
    # list_display = ('queastion_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(models.Question, QuestionAdmin)

class ChoiceInline(admin.StackedInline):
    model = models.Choice
    extra = 3
admin.site.register(models.Choice)
