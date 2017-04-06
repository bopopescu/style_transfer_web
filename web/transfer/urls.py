from django.conf.urls import url

from . import views

app_name = 'transfer'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$',views.upload,name='upload'),
    url(r'^output$',views.output,name='output'),
    url(r'^login$',views.login,name='login'),
    url(r'^tasks$',views.task_list,name='tasks'),
    url(r'^logout$',views.logout_view,name='login')
]