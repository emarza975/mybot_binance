from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('populate/', views.populate, name='populate'),
    path('stats/', views.stats, name='stats'),
    path('list_prices/', views.list_prices,name='list_prices' ),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('delete_prices/', views.delete_prices, name='delete_prices'),
    path('test_graph/', views.test_graph, name='test_graph'),
]