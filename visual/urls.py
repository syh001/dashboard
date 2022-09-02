from django.urls import path
from . import views
import pandas as pd


# 这句是必须的，和之后所有的URL语句有关
app_name = 'visual'

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('blog', views.blog, name = 'blog'),
    path('query', views.query, name = 'query'),
]