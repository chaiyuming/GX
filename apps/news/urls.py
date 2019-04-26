from django.urls import path
from . import views

app_name='news'
urlpatterns = [
    path('',views.NewsView.as_view(),name='news'),
    path('<int:news_id>/',views.NewsDetailView.as_view(),name='news_detail'),

]