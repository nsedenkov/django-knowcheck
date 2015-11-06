#! coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from userprofile.models import Pdrzd

class Settings(models.Model):
    name = models.CharField(u"Наименование", max_length=1024)
    qstn_cnt = models.IntegerField(u"количество вопросов", default=10)
    max_time = models.DurationField(u"Продолжительность", default=0)
    dt_create = models.DateTimeField("Created", default=timezone.now())

    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        ordering = ['-dt_create',]
        verbose_name = u"Вид тестировани"
        verbose_name_plural = u"Виды тестирования"

class Qstn(models.Model):
    q_text = models.CharField(u"Текст вопроса", max_length=4096)
    gid = models.ManyToManyField(Pdrzd, verbose_name=u'Подразделение')

    def __unicode__(self):
        return unicode(self.q_text)

    class Meta:
        ordering = ['q_text',]
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"

class Choice(models.Model):
    qstn = models.ForeignKey(Qstn, on_delete=models.CASCADE, verbose_name=u'Вопрос')
    c_text = models.CharField(u"Вариант ответа", max_length=4096)
    is_right = models.BooleanField(u"Верный вариант", default=False)

    def __unicode__(self):
        return unicode(self.c_text)

class UnFinManager(models.Manager):
    def get_query_set(self):
        return super(UnFinManager, self).get_query_set().filter(etm__isnull=True)
        
# Мастер-запись для сеанса тестирования
class LogMaster(models.Model):
    tst_id = models.ForeignKey(Settings)
    uid = models.ForeignKey(User)
    dt = models.DateTimeField("Testing date")
    etm = models.DateTimeField("End time", null=True)
    ws = models.GenericIPAddressField("IP", unpack_ipv4=True)
    # Менеджеры
    objects = models.Manager()
    ufobjects = UnFinManager()

# Список вопросов, выбранных для сеанса
class LogDetail(models.Model):
    mstr_id = models.ForeignKey(LogMaster)
    qstn = models.ForeignKey(Qstn)

# Список ответов, выбранных пользователем
class LogSubDetail(models.Model):
    det_id = models.ForeignKey(LogDetail)
    choice = models.ForeignKey(Choice)
