# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Pdrzd, Orgnz
 
 
class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'
 
# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline, )

class OrgnzAdmin(admin.ModelAdmin):
    fieldsets = [
                  (u'Подразделение', {'fields':['short_name', 'full_name'], 'classes':['wide']},),
                ]
    list_display = ('short_name', 'full_name',)
    search_fields = ['full_name',]

class PdrzdAdmin(admin.ModelAdmin):
    fieldsets = [
                  (u'Подразделение', {'fields':['name', 'orgnz'], 'classes':['wide']},),
                ]
    list_display = ('name', 'orgnz',)
    list_filter = ['orgnz']
    search_fields = ['name',]

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(Orgnz, OrgnzAdmin)
admin.site.register(Pdrzd, PdrzdAdmin)
admin.site.register(User, UserAdmin)