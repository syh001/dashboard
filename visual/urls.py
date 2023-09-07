from django.urls import path
from . import views

app_name = 'visual'  # 这句是必须的，和之后所有的URL语句有关
urlpatterns = [
    path('alert', views.alert, name="alert"),
    path('index', views.index, name='index'),
    path(r'query', views.query, name="query"),
    path(r'query1', views.query1, name="query1"),
    path('blog', views.blog, name = 'blog'),
    path(r'showdata', views.showdata, name="showdata"),
    path(r'plot', views.plot, name="plot"),
    path(r'get_process_name', views.get_process_name),


]




