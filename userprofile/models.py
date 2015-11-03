#! coding: utf-8
from django.db import models
from django.contrib.auth.models import User

class Orgnz(models.Model):
    short_name = models.CharField(u"Сокращенное наименование", max_length=128)
    full_name = models.CharField(u"Полное наименование", max_length=1024)

    def __unicode__(self):
        return self.short_name

    class Meta:
        verbose_name = u'Организация'
        verbose_name_plural = u'Организации'

class Pdrzd(models.Model):
    name = models.CharField(u"Наименование подразделения", max_length=128)
    orgnz = models.ForeignKey(Orgnz, on_delete=models.CASCADE, verbose_name=u'Организация')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Подразделение'
        verbose_name_plural = u'Подразделения'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    sur_name = models.CharField(u"Фамилия", max_length=64)
    first_name = models.CharField(u"Имя", max_length=64)
    patronimic = models.CharField(u"Отчество", max_length=64)
    position = models.CharField(u"Должность", max_length=256)
    pdrzd = models.ForeignKey(Pdrzd, on_delete=models.CASCADE, verbose_name=u'Подразделение')

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'