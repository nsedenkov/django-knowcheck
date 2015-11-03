#! coding: utf-8
from django.contrib import admin

from .models import Qstn, Choice, Settings

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QstnAdmin(admin.ModelAdmin):
    fieldsets = [
                  (u'Текст вопроса', {'fields':['q_text'], 'classes':['wide']},),
                  (u'Группа', {'fields':['gid'], 'classes':['wide']},),
                ]
    inlines = [ChoiceInLine]
    list_display = ('q_text',)
    list_filter = ['gid']
    search_fields = ['q_text',]

class SttngsAdmin(admin.ModelAdmin):
    fieldsets = [
                  (u'Вид тестирования', {'fields':['name', 'qstn_cnt', 'max_time'], 'classes':['wide']},),
                ]
    list_display = ('name', 'qstn_cnt', 'max_time',)
    search_fields = ['name',]

admin.site.register(Qstn, QstnAdmin)
admin.site.register(Settings, SttngsAdmin)
