#! coding: utf-8
from __future__ import division
import json
import datetime
import random
from urllib import unquote
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Qstn, Choice, Settings, LogMaster, LogDetail, LogSubDetail
from userprofile.models import UserProfile

class IndexView(generic.ListView):
    template_name = 'knowtest/index.html'
    context_object_name = 'all_tests_list'

    def get_queryset(self):
        return Settings.objects.all()

def ajax_send_test_by_id(request):
    if request.is_ajax():
        D = {}
        qexcnt = 0
        try:
            qexcnt = len(Qstn.objects.filter(gid=request.user.userprofile.pdrzd.id))
        except:
            qexcnt = -1
        t = Settings.objects.get(id=request.GET.get('id', 1))
        D['tm'] = str(t.max_time).split('.')[0]
        D['qc'] = t.qstn_cnt
        D['ec'] = qexcnt
        return JsonResponse(D)
    else:
        return JsonResponse({}, status=400)

@login_required
def starttest(request):
    if 't_id' in request.GET and request.GET['t_id']:
        # проверить, есть ли незавершенное тестирование
        #log_m = LogMaster.objects.filter(pk=u_id)
        # Список для id выбранных вопросов - selected questions
        s_qstn = []
        valid_qstn = []
        cur_set = Settings.objects.get(pk=request.GET['t_id'])
        q_lst = Qstn.objects.filter(gid=user_group()).order_by('id')
        for q in q_lst:
            valid_qstn.append(q.id)
        while len(s_qstn) < cur_set.qstn_cnt:
            x = random.randint(valid_qstn[0], valid_qstn[len(valid_qstn)-1])
            if x not in s_qstn and x in valid_qstn:
                s_qstn.append(x)
        lm = LogMaster(tst_id=cur_set, uid=request.user, dt=timezone.now(), ws=request.META.get('REMOTE_ADDR', '0.0.0.0'))
        lm.save()
        for x in s_qstn:
            ld = LogDetail(mstr_id=lm, qstn=Qstn.objects.get(pk=x))
            ld.save()
        return HttpResponseRedirect('/knowtest/process/?t_id=%s' % lm.id)
    else:
        # Вернуть на index.html с сообщением об ошибке
        return render_to_response('')

@login_required
def processtest(request):
    if 't_id' in request.GET and request.GET['t_id']:
        return render(request, 'knowtest/detail.html', {'test_id': request.GET['t_id']})
    else:
        return render(request, 'knowtest/detail.html', {'no_test_id': 'ERROR'})

def ajax_send_qstn_first(request):
    # Возвращает список id вопросов по id текущего сеанса тестирования
    if request.is_ajax() and 't_id' in request.GET and request.GET['t_id']:
        D = {}
        i = 0
        for q in LogDetail.objects.filter(mstr_id=LogMaster.objects.get(pk=request.GET['t_id'])):
            key = 'q%s' % i
            D[key] = q.qstn.id
            i += 1
        return JsonResponse(D)
    else:
        return JsonResponse({}, status=400)

def ajax_send_one_qstn(request):
    # Возвращает текст вопроса, варианты ответов, варианты, выбранные пользователем и признак multi
    if request.is_ajax() and 'q_id' in request.GET and 't_id' in request.GET and request.GET['q_id']  and request.GET['t_id']:
        D = {}
        subD = {}
        resD = {}
        qstn = Qstn.objects.get(pk=request.GET['q_id'])
        D['q_txt'] = qstn.q_text
        # Список вариантов ответа
        y = 0 # Счетчик верных вариантов ответа
        for choice in qstn.choice_set.all():
            key = choice.id
            subD[key] = choice.c_text
            if choice.is_right:
                y += 1
        D['choices'] = subD
        if y > 1:
            D['multi'] = 1
        # Выборы пользователя
        ld = LogDetail.objects.filter(mstr_id=LogMaster.objects.get(pk=request.GET['t_id'])).filter(qstn=request.GET['q_id'])
        i = 0
        for lsd in LogSubDetail.objects.filter(det_id=ld):
            resD[i] = lsd.choice.id
            i += 1
        D['answers'] = resD
        return JsonResponse(D)
    else:
        return JsonResponse({}, status=400)

def ajax_post_answers(request):
    if request.is_ajax() and 'q_id' in request.GET and 't_id' in request.GET and request.GET['q_id']  and request.GET['t_id']:
        ld = LogDetail.objects.filter(mstr_id=LogMaster.objects.get(pk=request.GET['t_id'])).get(qstn=request.GET['q_id'])
        q = json.loads(unquote(request.GET['c_id']))
        for j in q:
            for key in j.keys():
                c = Choice.objects.get(pk=j[key])
                lsd = LogSubDetail(det_id=ld, choice=c)
                lsd.save()
        # Определить и вернуть к-во оставшихся вопросов
        tot_q_cnt = ld.mstr_id.tst_id.qstn_cnt
        cmplt_q = []
        for lds in ld.mstr_id.logdetail_set.all():
            for lsd in lds.logsubdetail_set.all():
                if lsd.det_id.id not in cmplt_q:
                    cmplt_q.append(lsd.det_id.id)
        return JsonResponse({'q_elps': tot_q_cnt-len(cmplt_q)})
    else:
        return JsonResponse({}, status=400)

def ajax_send_cur_time(request):

    def timedelta_to_seconds(td):
        return td.seconds + td.days*24*60*60

    if request.is_ajax() and 't_id' in request.GET and request.GET['t_id']:
        D = {}
        # Текущее время для текущего часового пояса (make_naive)
        tmn = timezone.make_naive(timezone.now())
        D['ctm'] = '%02i:%02i:%02i' % (tmn.hour, tmn.minute, tmn.second)
        # Достать время начала теста и определить, сколько осталось
        lm = LogMaster.objects.get(pk=request.GET['t_id'])
        # Ожидаемое время завершения (время начала + заданный интервал из Settings)
        endtime = timezone.make_naive(lm.dt) + lm.tst_id.max_time
        # Оставшееся время
        if endtime >= tmn:
            elapsed = endtime - tmn
            if timedelta_to_seconds(elapsed) > 0:
                D['etm'] = str(elapsed).split('.')[0]
            else:
                D['etm'] = 0
        else:
            D['etm'] = 0
        return JsonResponse(D)
    else:
        return JsonResponse({}, status=400)

def finish_test(request):
    if 't_id' in request.GET and request.GET['t_id']:
        lm = LogMaster.objects.get(pk=request.GET['t_id'])
        lm.etm = timezone.now()
        lm.save()
        return HttpResponseRedirect('/knowtest/results/')
    else:
        return render_to_response()

@login_required
def show_results(request):
    res = []
    lm_all = LogMaster.objects.filter(uid=request.user).order_by('-dt')
    for lm in lm_all:
        D = {}
        D['t_id'] = lm.id
        D['name'] = lm.tst_id.name
        dtn = timezone.make_naive(lm.dt)
        D['date'] = '%02i.%02i.%04i %02i:%02i' % (dtn.day, dtn.month, dtn.year, dtn.hour, dtn.minute)
        D['ip'] = lm.ws
        res.append(D)
    if len(res) > 0:
        return render(request, 'knowtest/results.html', {'res': res})
    else:
        return render(request, 'knowtest/results.html', {})

@login_required
def show_one_result(request):
    if 't_id' in request.GET and request.GET['t_id']:
        main = {} # Для имени, должности и т.д.
        q_set = []
        right_count = 0
        lm = LogMaster.objects.get(pk=request.GET['t_id'])
        up = UserProfile.objects.get(user_id=lm.uid_id)
        dtn = timezone.make_naive(lm.dt)
        etm = timezone.make_naive(lm.etm)
        main['fio'] = up.sur_name + ' ' + up.first_name + ' ' + up.patronimic
        main['fio_srt'] = up.sur_name + ' ' + up.first_name[0] + '.' + up.patronimic[0]+'.'
        main['org'] = up.pdrzd.orgnz.full_name
        main['pdrz'] = up.pdrzd.name
        main['dlgn'] = up.position
        main['date'] = '%02i.%02i.%04i' % (dtn.day, dtn.month, dtn.year)
        main['btm'] = '%02i:%02i:%02i' % (dtn.hour, dtn.minute, dtn.second)
        main['etm'] = '%02i:%02i:%02i' % (etm.hour, etm.minute, etm.second)
        lds = LogDetail.objects.filter(mstr_id=lm)
        for ld in lds:
            D = {}
            c_set = [] # список выбранных вариантов
            D['qstn'] = ld.qstn.q_text
            is_right = 0
            for lsd in ld.logsubdetail_set.all():
                c_one = {} # текст варианта + статус (верно/неверно)
                c_one['txt'] = lsd.choice.c_text
                if lsd.choice.is_right:
                    c_one['res'] = u'Верно'
                    is_right = 1
                else:
                    c_one['res'] = u'Неверно'
                    is_right = 0
                c_set.append(c_one)
            right_count += is_right
            D['ans'] = c_set
            if is_right > 0:
                D['q_res'] = u'Верно'
            else:
                D['q_res'] = u'Неверно'
            q_set.append(D)
        tot_res = right_count / len(lds) * 100
        return render(request, 'knowtest/result.html', {'main':main, 'q_set':q_set, 'r_cnt':right_count, 'tot_res':tot_res})
    else:
        return render(request, 'knowtest/err404.html')