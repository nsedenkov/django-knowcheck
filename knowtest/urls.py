from django.conf.urls import url

from . import views

urlpatterns = [
                # ex: /knowtest/
                url(r'^$', views.IndexView.as_view(), name='index'),
                # ex: /gettest/
                url(r'^gettest/$', views.ajax_send_test_by_id, name='alltests'),
                url(r'^gettime/$', views.ajax_send_cur_time, name='send_time'),
                url(r'^start/$', views.starttest, name='start'),
                url(r'^process/$', views.processtest, name='process'),
                url(r'^finish/$', views.finish_test, name='finish'),
                url(r'^results/$', views.show_results, name='results'),
                url(r'^result/$', views.show_one_result, name='one_result'),
                # ex: /getdetail/?t_id=156
                url(r'^getdetail/$', views.ajax_send_qstn_first, name='sel_qstns'),
                # ex: /getsubdetail/?q_id=23
                url(r'^getsubdetail/$', views.ajax_send_one_qstn, name='send_qstn'),
                url(r'^fixanswer/$', views.ajax_post_answers, name='post_answ'),
]